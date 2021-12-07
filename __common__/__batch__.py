import subprocess as sp

def batchCommand(*args):
    a = sp.Popen(args[0], shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)        
    try : 
        output, error = a.communicate(timeout=args[1])
    except:
        output, error = a.communicate()
            #return ['Another Except'], ['Another Except']
        
    if output != []:
        output =  [v for v in output.split('\n') if v]        
    else:
        output = []
    if error != []:
        error =  [v for v in error.split('\n') if v]
    else:
        error = []

    return output, error