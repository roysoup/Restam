#!/bin/env/python3
# coding: utf8

"""I'm a neglected docstring!!"""

__version__ = ""
__author__ = "Roy Siu"
__credits = []

from pathlib import Path
from typing import Dict, Tuple, List, Any, Callable
import sys

## Create type signatures
meal_config_typing = Dict[ str, Any ]
meals_config_typing = Dict[ str, meal_config_typing ]

meals_data_typing = Dict[ str, int ]

### Decorators

def check_iden_exists( func:Callable, *args, **kwargs ):
    def _inner( self, *args, **kwargs ):
        try:
            if not ( isinstance(kwargs["iden"], int) ):
                raise ValueError("iden is not str")
            if not ( kwargs["iden"] in self.transactions ):
                raise ValueError("iden does not exist")
        except ValueError as e:  # Catch-all
            print( "Error in {0}: {1}".format( func, e.args ) )
            raise  # Re-raise error for handling
        else:
            return func( self, **kwargs )
    return _inner

### Classes

class Transaction( object ):
    def __init__( self ):
        self.transactions = {}
        self.next_transaction_no = 0
    
    @property
    def pending_transcations(self) -> dict:
        pending = {}
        for transaction in self.transactions:
            if self.transactions[transaction].pending:
                pending[transaction] = self.transactions[transaction]
        return pending
    
    @property
    def completed_transcations(self) -> dict:
        completed = {}
        for transaction in self.transactions:
            if self.transactions[transaction].complete:
                completed[transaction] = self.transactions[transaction]
        return completed
    
    @property
    def cancelled_transcations(self) -> dict:
        cancelled = {}
        for transaction in self.transactions:
            if self.transactions[transaction].cancelled:
                cancelled[transaction] = self.transactions[transaction]
        return cancelled

class Restaurant( Transaction ):
    
    def __init__( self, *args ) -> None:
        """Initiate restaurant object with config_files (args)"""
        
        self.timing_interval_mins = 1
        
        self.restaurant_name = "NAME"
        
        self.opening_time = [00, 00]
        self.final_orders = [00, 00]
        self.closing_time = [00, 00]
        self.max_stay = 0
        
        self.floors_and_tables_config = {}
        self.common_table_joins_config = {}
        
        self.meals = {}
        
        for config_file in args:
            with config_file.open() as f:
                exec( f.read() )
        
        try:
            ## Main configs
            if not (type(self.timing_interval_mins) is int):
                raise TypeError("self.timing_interval_mins is not int")
            
            if not (type(self.restaurant_name) is str):
                raise TypeError("self.restaurant_name is not str")
            
            for times in (self.opening_time, self.final_orders, self.closing_time):
                if not (type(times) is int):
                    raise TypeError("'{}' not integer".format(times))
            
            if not (type(self.floors_and_tables_config) is dict):
                raise TypeError("self.floors_and_tables is not dict")
            for floor_key in self.floors_and_tables_config.keys():  # Check valid floor and table config format
                if not (type( self.floors_and_tables_config[floor_key] ) is list):
                    raise TypeError("floor index {0} is not a list".format( floor_key ))
                for table_key, table in enumerate( self.floors_and_tables_config[floor_key] ):
                    """kt = frozenset((floor_key, table_key))
                    for to_check, type_, error_message in map(
                            [type(table), len(table), type(table[0]), type(table[1])],
                            [list, 2, int, int],
                            ["table index '{1}', floor index '{0}': is not a list".format(*kt),
                            "table index '{1}', floor index '{0}': list length not 2".format(*kt),
                            "table index '{1}', floor index '{0}': table number (index 0) not int".format(*kt),
                            "table index '{1}', floor index '{0}': seat count (index 0) not int".format(*kt)]
                            ):
                        print(to_check, type_, error_message)
                        if not (to_check is type_):
                            raise TypeError(error_message)"""
                    assert type(table) is list , "table index '{1}', floor index '{0}': is not a list".format( floor_key, table_key )
                    assert len(table) is 2 , "table index '{1}', floor index '{0}': list length not 2".format( floor_key, table_key )
                    
                    assert type( table[0] ) is int , "table index '{1}', floor index '{0}': table number (index 0) not int".format( floor_key, table_key )
                    assert type( table[1] ) is int , "table index '{1}', floor index '{0}': seat count (index 0) not int".format( floor_key, table_key )
            
            if not (type(self.common_table_joins_config) is dict):
                raise TypeError("self.common_table_joins is not dict")
                
            ## Meals
            if not (type(self.meals) is dict):
                raise TypeError("self.meals is not dict")
            for meal_key, meal_details in self.meals.items():
                if not (type(meal_key) is str):
                    raise TypeError("meal key {0} not str".format( meal_key ))
                if not (type(meal_details) is dict):
                    raise TypeError("meal key '{0}': details not dict".format( meal_key ))
                for i in ( "name", "price", "veg", "egg_free", "dairy_free", "nut_free" ):
                    if not (i in meal_details):
                        raise TypeError("meal key '{0}': does not specify {1}".format( meal_key, i ))
                
                if not (type(meal_details["name"]) is str):
                    raise TypeError("meal key '{0}', detail key '{1}': {2} is not str".format( meal_key, "name", meal_details["name"] ))
                if not (type(meal_details["price"]) is float):
                    raise TypeError("meal key '{0}', detail key '{1}': {2} is not int".format( meal_key, "price", meal_details["price"] ))
                if not (meal_details["veg"] in ( 0, 1, 2, None )):
                    raise TypeError("meal key '{0}', detail key '{1}': {2} not in ( 0, 1, 2, None )".format( meal_key, "veg", meal_details["veg"] ))
                if not (meal_details["egg_free"] in ( True, False, None )):
                    raise TypeError("meal key '{0}', detail key '{1}': {2} is not bool or None".format( meal_key, "egg_free", meal_details["egg_free"] ))
                if not (meal_details["dairy_free"] in ( True, False, None )):
                    raise TypeError("meal key '{0}', detail key '{1}': {2} is not bool or None".format( meal_key, "dairy_free", meal_details["dairy_free"] ))
                if not (meal_details["nut_free"] in ( True, False, None )):
                    raise TypeError("meal key '{0}', detail key '{1}': {2} is not bool or None".format( meal_key, "nut_free", meal_details["nut_free"] ))
            
        except TypeError as e:
            print( "Error in {0}: {1}".format( sys._getframe().f_code.co_name, e.args ) )
            raise  # Re-raise error for handling
        
        else:
            super().__init__()
            
            ## Timetable generation
            self.timetable = {}
            open_hour, open_min = divmod( self.opening_time, 100 )
            close_hour, close_min = divmod( self.closing_time, 100 )
            total_open_time_mins = ( close_hour - open_hour ) * 60  +  ( close_min - open_min )
            for momentx5 in range( 0, total_open_time_mins, self.timing_interval_mins ):
                self.timetable[ int(momentx5/5) ] = None
            
            ## Floor dictionary generation
            self.floors = {}
            for floor_no, table_list in self.floors_and_tables_config.items():  # need to error check
                self.floors[str(floor_no)] = Floor( table_list )
    
    def time_to_moment( self, time ):
        try:
            if ( time < self.opening_time ) or ( time > self.closing_time ):
                raise ValueError( "time ({2}) not between opening times: {0} and {1}".format( self.opening_time, self.closing_time, time ) )
            if ( ( time - self.opening_time ) % self.timing_interval_mins ) != 0:
                raise ValueError( "time ({2}) is not at an interval of {0} mins from opening time ({1})".format( self.timing_interval_mins, self.opening_time, time ) )
        except ValueError as e:
            print( "Error in {0}: {1}".format( sys._getframe().f_code.co_name, e.args ) )
            raise # Re-raise error for handling
        else:
            open_hour, open_min = divmod( self.opening_time, 100 )
            time_hour, time_min = divmod( time, 100 )
            return int(  ( ( time_hour - open_hour ) * 60  +  ( time_min - open_min ) ) / self.timing_interval_mins  )
    
    def moment_to_time( self, moment ):
        hour_add, min_add = divmod( moment * self.timing_interval_mins, 60 )
        to_add = hour_add * 100 + min_add
        return int( self.opening_time + to_add )
    
    def add_party( self, time_start:int, meals:dict, booked:bool,
            name:str="anon", caravan_no:int=-1, telephone_no:int=-1, additional_notes:str="" ) -> "Restaurant":
        time_length = self.max_stay  # Need error check in init
        try:
            if not (type(meals) is dict):
                raise TypeError("meals is not dict")
            for key, value in meals.items():
                if not (type(key) is str):
                    raise TypeError("meals key '{0}' not str".format( key ))
                if not (type(value) is int):
                    raise TypeError("meals key '{0}': value not int".format( key ))
            
            if not (type(booked) is bool):
                raise TypeError("booked not int")
            if not (type(name) is str):
                raise TypeError("name not str")
            if not (type(caravan_no) is int):
                raise TypeError("caravan_no not int")
            if not (type(telephone_no) is int):
                raise TypeError("telephone_no not int")
            if not (type(additional_notes) is str):
                raise TypeError("additional_notes not str")
        except TypeError as e:
            print( "Error in {}".format(sys._getframe().f_code.co_name), e.args )
            raise  # Re-raise error for handling
        else:
            self.transactions[ self.next_transaction_no ] = Party( time_start=time_start, time_length=time_length,
                    meals=meals, booked=booked, name=name,
                    caravan_no=caravan_no, telephone_no=telephone_no, additional_notes=additional_notes )
            self.__add_party_to_timetable( self.next_transaction_no )
            self.next_transaction_no += 1
    
    def __add_party_to_timetable( self, iden:str ) -> bool:
        start_moment = self.time_to_moment( self.transactions[iden].time_start )
        start_timeframe = self.timetable[start_moment]
        #self.timetable[start_moment] = self.transactions[iden] #testing
    
    @check_iden_exists
    def modify_meals( self, iden:str, meals_add:Dict[ str, int ] ) -> None:
        """ modify amount of meals in a party/booking order
        iden -- the party that the prices should be added to
        meals_add -- dictionary where key is the meal (normally a number), and the value is the amount to be added (to remove, use negative value)
        """
        try:
            self.transactions[iden].modify_meals(meals_add)
        except TypeError as e:
            print( "Error in {}".format(sys._getframe().f_code.co_name), e.args )
            raise  # Re-raise error for handling
    
    @check_iden_exists
    def overwrite_additional_party_notes( self, iden:int, notes:str, mode:str="w" ) -> None:
        try:
            if not ( mode in ( "w", "a" ) ):
                raise ValueError( "invalid mode: '{}'".format(mode) )
        except ( TypeError, KeyError, ValueError ) as e:
            print( "Error in {}".format(sys._getframe().f_code.co_name), e.args )
            raise  # Re-raise error for handling
        else:
            self.transactions[iden].overwrite_additional_party_notes( notes=notes, mode=mode )
    
    @check_iden_exists
    def modify_past_meals( self, iden:str, meals_add:meals_data_typing ) -> None:
        """Modify meals on a completed transaction"""
        pass
    
    ## Status manipulation
    @check_iden_exists
    def get_party( self, iden:int ) -> dict:
        return self.transactions[iden]
    
    def search_parties( self, category, search_term ):
        pass
    
    @check_iden_exists
    def complete_party( self, iden:int ) -> None:
        self.transactions[iden].complete = True
    @check_iden_exists
    def cancel_party( self, iden ):
        self.transactions[iden].cancelled = True
    @check_iden_exists
    def reactivate_party( self, iden ):
        self.transactions[iden].pending = True
    
    def hcf( self ):
        pass

class Party( Restaurant ):
    
    def __init__( self, time_start:int, time_length:int, meals:dict, booked:bool,
            name:str="anon", caravan_no:int=-1, telephone_no:int=-1, additional_notes:str="", status:int=0 ) -> None:
        self.time_start = time_start
        self.time_length = time_length
        self.meals = meals
        self.name = name
        self.caravan_no = caravan_no
        self.telephone_no = telephone_no
        self.additional_notes = additional_notes
        self.status = status
        self.status_log = [status]
    
    ## Status properties
    
    @property
    def time_end(self):
        return self.time_start + self.time_length
    
    @property
    def pending(self):
        return ( self.status == 0 )
    @pending.setter
    def pending( self, value ):
        if value:
            self.status = 0
            self.status_log.append(0)
        else:
            raise ValueError
    
    @property
    def complete(self):
        return ( self.status == 1 )
    @complete.setter
    def complete( self, value ):
        if value:
            self.status = 1
            self.status_log.append(1)
        else:
            raise ValueError
    
    @property
    def cancelled(self):
        return ( self.status == 2 )
    @cancelled.setter
    def cancelled( self, value ):
        if value:
            self.status = 2
            self.status_log.append(2)
        else:
            raise ValueError
    
    def modify_meals( self, meals_add:meals_data_typing ) -> None:
        """ modify amount of meals in a party/booking order
        iden -- the party that the prices should be added to
        meals_add -- dictionary where key is the meal (normally a number), and the value is the amount to be added (to remove, use negative value)
        """
        for meal, amount in meals_add.items():
            self.meals[meal] = self.meals.get( meal, 0 ) + amount
    
    def overwrite_additional_party_notes( self, notes:str, mode:str="w" ) -> None:
        if mode == "w": self.additional_notes = notes
        elif mode == "a": self.additional_notes += notes

class Floor( Restaurant ):
    
    def __init__( self, tables ) -> None:
        self.tables = {}
        for table in tables:
            self.tables[ str(table[0]) ] = Table( table[1] )

class Table( Floor ):
    
    def __init__( self, seats:int ) -> None:
        self.seats = seats

if __name__ == "__main__":
    from pprint import pprint
    import sys
    print( ".".join( [str(info) for info in sys.version_info]) )
    
    # instantiate
    main = Path('../haggerston_main.cfg')
    meals = Path('../haggerston_meals.cfg')
    drinks = Path('../haggerston_drinks.cfg')
    takeaways = Path('../haggerston_takeaways.cfg')
    
    # add bookings
    test = Restaurant( main, meals, drinks, takeaways )
    
    # add to doctest
    #print(test.timetable)
    #print(test.time_to_moment(1630))
    #print(test.time_to_moment(2255))
    #print(test.time_to_moment(2300))
    
    test.add_party( meals={ "1":3, "2":1}, time_start=1830, booked=True, name="the first 3 guys and a kid" )
    test.add_party( meals={"1":1}, booked=True, time_start=1845, name="a lonely guy" )
    
    import doctest
    
    #doctest.testfile("bookings_restam.doctest")
