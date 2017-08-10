
def nargs(args, **kwargs):
  ''' Filter **kwargs removing nulls and args we don't want '''
  return {k: v for k, v in kwargs.items()
          if v is not None and k in args}
