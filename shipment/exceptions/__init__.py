import sys
import os

#sys is a built-in Python module that provides access to system-specific parameters and functions. You can use it to interact with the Python interpreter.

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info() 
    file_name=exc_tb.tb_frame.f_code.co_filename

    error_message="Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )

    return error_message



#exc.info() ->It returns a tuple of three values:
#type: the type of the exception (e.g., ZeroDivisionError, ValueError)
#value: the actual exception object (the error message)
#traceback: a traceback object that helps you trace where the error occurred (which file and line)



class shippingException(Exception):
    def __init__(self,error_message,error_detail: sys):
        super().__init__(error_message)
        self.error_message= error_message_detail(
            error_message,error_detail=error_detail
        )

    def __str__(self):
        return self.error_message