def muTrigScale_MuEG_2012_53X(mupt, mueta):

  if( 10.0 < mupt and mupt <= 15.0 ):
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8):    return 0.9829
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9745
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9943
    elif( 1.6 <= abs(mueta) ):                      return 0.9158
    
  elif( 15.0 < mupt and mupt <= 20.0 ):
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9850
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9852
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9743
    elif( 1.6 <= abs(mueta) ):                      return 0.9333 

  elif( 20.0 < mupt and mupt <= 25.0 ):		          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9951
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9610
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9716
    elif( 1.6 <= abs(mueta) ):                      return 0.9459 

  elif( 25.0 < mupt and mupt <= 30.0 ):		          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9869
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9779
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9665
    elif( 1.6 <= abs(mueta) ):                      return 0.9501 

  elif( 30.0 < mupt and mupt <= 35.0 ):		          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9959
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9881
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9932
    elif( 1.6 <= abs(mueta) ):                      return 0.9391 

  else:							          
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):   return 0.9986
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ): return 0.9540
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ): return 0.9549
    elif( 1.6 <= abs(mueta) ):                      return 0.9386 

  return 0.



def eleTrigScale_MuEG_2012_53X(elept, eleeta):

  if( 10.0 < elept and elept <= 15.0 ):
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9548
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9015
    elif( 1.5 <= abs(eleeta) ):                      return 0.9017 

  elif( 15.0 < elept and elept <= 20.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9830
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9672
    elif( 1.5 <= abs(eleeta) ):                      return 0.9463 

  elif( 20.0 < elept and elept <= 25.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9707
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9731
    elif( 1.5 <= abs(eleeta) ):                      return 0.9691 

  elif( 25.0 < elept and elept <= 30.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9768
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9870
    elif( 1.5 <= abs(eleeta) ):                      return 0.9727 

  elif( 30.0 < elept and elept <= 35.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 1.0047
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9891
    elif( 1.5 <= abs(eleeta) ):                      return 0.9858 

  else:
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 1.0063
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 1.0047
    elif( 1.5 <= abs(eleeta) ):                      return 1.0015 

  return 0.



def eleIDscale_MuEG_2012_53X(elept, eleeta):
  if( 10.0 < elept and elept <= 15.0 ):	
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.7654
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.7693  
    elif( 1.5 <= abs(eleeta) ):                      return 0.5719  

  elif( 15.0 < elept and elept <= 20.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.8394
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.8457 
    elif( 1.5 <= abs(eleeta) ):                      return 0.7024  

  elif( 20.0 < elept and elept <= 25.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.8772
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.8530  
    elif( 1.5 <= abs(eleeta) ):                      return 0.7631  

  elif( 25.0 < elept and elept <= 30.0 ):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9006
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.8874 
    elif( 1.5 <= abs(eleeta) ):                      return 0.8092  

  elif( 30.0 < elept and elept <= 35.0):		            
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9261
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9199  
    elif( 1.5 <= abs(eleeta) ):                      return 0.8469  

  else:
    if( 0.0 <= abs(eleeta) and abs(eleeta) < 0.8 ):      return 0.9514
    elif( 0.8 <= abs(eleeta) and abs(eleeta) < 1.5 ): return 0.9445 
    elif( 1.5 <= abs(eleeta) ):                      return 0.9078  

  return  0.



def muIDscale_MuEG_2012_53X(mupt, mueta):

  if( 10.0 < mupt and mupt <= 15.0 ):
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):       return 0.9771
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9746  
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ):  return 0.9644  
    elif( 1.6 <= abs(mueta) ):                      return 0.9891  

  elif( 15.0 < mupt and mupt <= 20.0 ):		           
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):       return 0.9548
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9701 
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ):  return 0.9766 
    elif( 1.6 <= abs(mueta) ):                      return 0.9892  

  elif( 20.0 < mupt and mupt <= 25.0 ):		           
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):       return 0.9648
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9836
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ):  return 0.9820
    elif( 1.6 <= abs(mueta) ):                      return 0.9909 

  elif( 25.0 < mupt and mupt <= 30.0 ):		           
    if ( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):      return 0.9676
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9817 
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ):  return 0.9886 
    elif( 1.6 <= abs(mueta) ):                      return 0.9883  

  elif( 30.0 < mupt and mupt <= 35.0 ):		           
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):       return 0.9730
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9833 
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ):  return 0.9910 
    elif( 1.6 <= abs(mueta) ):                      return 0.9900  

  else:
    if( 0.0 <= abs(mueta) and abs(mueta) < 0.8 ):       return 0.9826
    elif( 0.8 <= abs(mueta) and abs(mueta) < 1.2 ):  return 0.9841 
    elif( 1.2 <= abs(mueta) and abs(mueta) < 1.6 ):  return 0.9900 
    elif( 1.6 <= abs(mueta) ):                      return 0.9886  

  return 0.

