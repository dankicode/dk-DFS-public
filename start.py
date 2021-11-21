import optimizer as optimizer
import config as config


for conf in config.getConfig():
  print('---------------------------------------\n')
  print("creating lineup for: %s with manual overides: %s"%(conf['projectionType'], conf['preProcess']))
  optimizer.createLineups(conf)