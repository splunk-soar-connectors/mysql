# --
# File: mysql_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
# from mysql_consts import *
import re
import csv
import json
import mysql.connector


class RetVal(tuple):
    def __new__(cls, val1, val2):
        return tuple.__new__(RetVal, (val1, val2))


class MysqlConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(MysqlConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None
        self._my_connection = None

    def _cleanup_row_values(self, row):
        # The MySQL column values is supposed to be a bytearray as opposed to a string
        return {k: v.decode('utf-8') if type(v) == bytearray else v for k, v in row.iteritems()}

    def _handle_test_connectivity(self, param):

        # Add an action result object to self (BaseConnector)
        # to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Testing database connection")
        cursor = self._my_connection.cursor()

        query = ("SELECT version()")

        cursor.execute(query)
        if cursor:
            self.save_progress("Test Connectivity Passed")
            return action_result.set_status(phantom.APP_SUCCESS)
        else:
            return action_result.set_status(phantom.APP_ERROR,
                                            "Connection failed")

    def _handle_list_columns(self, param):

        self.save_progress("In action handler for: {0}".format(
            self.get_action_identifier()))

        # Add an action result object to self (BaseConnector)
        # to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        my_table = param['table_name']
        if not re.match(r'^[a-zA-Z0-9$_]+$', my_table):
            return action_result.set_status(phantom.APP_ERROR, "Table name did not pass validation")
        query = "DESCRIBE {0};".format(my_table)
        cursor = self._my_connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Unable to list columns", e
            )

        for row in cursor:
            action_result.add_data(self._cleanup_row_values(row))

        summary = action_result.update_summary({})
        summary['total_rows'] = cursor.rowcount

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_list_tables(self, param):

        self.save_progress("In action handler for: {0}".format(
            self.get_action_identifier()))

        # Add an action result object to self (BaseConnector)
        # to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        query = "SHOW TABLES;"
        cursor = self._my_connection.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            row = self._cleanup_row_values(row)
            # Rename column name so it will be the same for every asset
            #  running the app
            # There should only be one column per row, but let's double check first
            if len(row) == 1:
                row = dict(table_name=next(row.itervalues()))
            action_result.add_data(row)

        summary = action_result.update_summary({})
        summary['total_rows'] = cursor.rowcount

        return action_result.set_status(phantom.APP_SUCCESS)

    def _get_format_vars(self, param):
        format_vars = param.get('format_vars')
        if format_vars:
            format_vars = csv.reader([format_vars], quotechar='"', skipinitialspace=True, escapechar='\\').next()
        return format_vars

    def _handle_run_query(self, param):
        self.save_progress("In action handler for: {0}".format(
            self.get_action_identifier()))

        # Add an action result object to self (BaseConnector)
        # to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        my_query = param.get('query')
        format_vars = self._get_format_vars(param)

        cursor = self._my_connection.cursor(dictionary=True)
        try:
            cursor.execute(my_query, format_vars)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Unable to run query", e
            )

        for row in cursor:
            action_result.add_data(self._cleanup_row_values(row))

        if not param.get('no_commit', False):
            try:
                self._my_connection.commit()
            except Exception as e:
                return action_result.set_status(
                    phantom.APP_ERROR, "Unable to commit changes", e
                )

        summary = action_result.update_summary({})

        # cursor.rowcount returns -1 if no rows returned
        if cursor.rowcount > 0:
            summary['total_rows'] = cursor.rowcount
        else:
            summary['total_rows'] = 0

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully ran query")

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'list_columns':
            ret_val = self._handle_list_columns(param)

        elif action_id == 'list_tables':
            ret_val = self._handle_list_tables(param)

        elif action_id == 'run_query':
            ret_val = self._handle_run_query(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        # Access values in asset config by the name

        # Required values can be accessed directly
        # required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        # optional_config_name = config.get('optional_config_name')

        self.save_progress("Starting db initialization")
        try:
            self._my_connection = mysql.connector.connect(user=config['username'],
                                                          password=config['password'],
                                                          database=config['database'],
                                                          host=config['host'])
            # self._my_connection.autocommit = True
        except mysql.connector.Error as err:
            if self.get_action_identifier() == "test_connectivity":
                self.save_progress("db login error")
                self.save_progress(str(err))
                self.set_status(phantom.APP_ERROR, "Test Connectivity Failed")
            else:
                self.set_status(phantom.APP_ERROR, "db login error", err)
            return False
        self.save_progress("Database connection established")
        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import sys
    import pudb
    pudb.set_trace()

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = MysqlConnector()
        connector.print_progress_message = True
        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
