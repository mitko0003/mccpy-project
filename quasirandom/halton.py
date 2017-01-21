 def __bootstrap__():                                             
   global __bootstrap__, __loader__, __file__                     
   import sys, pkg_resources, imp                                 
   __file__ = pkg_resources.resource_filename(__name__,'halton.so')
   __loader__ = None; del __bootstrap__, __loader__               
   imp.load_dynamic(__name__,__file__)                            
                                                                  
if __name__ != "__main__":                                        
    __bootstrap__()                                               
