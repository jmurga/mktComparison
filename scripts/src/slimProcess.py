#!/home/jmurga/.conda/envs/simulations/bin/python
######################################################################
###############SCRIPT TO AUTOMATIZE SLIM SIMULATIONS##################
#####################CREATES TEMPORAL RECIPES#########################
##############BASED ON THE SELECTED RECIPE AND ARGPARSE MODULE########
########MODIFIED FROM https://github.com/bodkan/nea-over-time#########
######################################################################
import argparse
import sys
import os
import random
import subprocess
import pandas as pd
# import rpy2
# import rpy2.robjects as robjects
from string import Template
from tempfile import NamedTemporaryFile
# from rpy2 import robjects
# from rpy2.robjects import pandas2ri

# pandas2ri.activate()


# Write lists to an .RData file. Two functions in order to save differents global variable name.
def saveRdata(ls,filename,path,variableName):
	robjects.r.assign('{}', robjects.Vector(ls)).format(variableName)
	robjects.r("save({}, file='{}{}')".format(variableName,path,filename))


def slimVector(xs):
	"""Convert a list of numbers to a SLiM code creating the same list."""
	return "c(" + ",".join(str(x) for x in xs) + ")"

if __name__ == "__main__":
	'''Parse arguments and show the required inputs if only name is given to command line'''
	parser = argparse.ArgumentParser(description="SLiM simulations based on baseline recipe extract from asymptoticMK github, based on Messer et al 2013.")

	# Required arguments
	parser.add_argument("--recipe", type = str, required = True, help = "Slim recipe to execute",choices=['baseline'])
	parser.add_argument("--length", type = float, required = 1e7, help = "0-based start and stop SLiM length to simulate.")
	parser.add_argument("--mutRate", type = float, required = 1e-9, help = "Mutation rate in the simulated region")
	parser.add_argument("--recombRate", type = float, required = 1e-7, help = "Recombination rate in the simulated region")
	parser.add_argument("--dominanceCoef", type = float, required = 0.5, help = "")
	parser.add_argument("--rb", type = float, required = 0.0005, help = "")
	parser.add_argument("--sd", type = float, required = 0.1, help = "")
	parser.add_argument("--sb", type = float, required = 0.2, help = "")
	parser.add_argument("--ancSize", type = int, required = 1000, help = "Effective population size of the ancestral population")
	parser.add_argument("--burnin", type = int, required = 10000, help = "Burnin period")
	parser.add_argument("--generations", type = int, required = 210000, help = "Burnin period")
	parser.add_argument("--bins", type = int, required = 20, help = "Burnin period")
	parser.add_argument("--replica", type = int, required = 20, help = "Number of replica by scenario")

	parser.add_argument("--output", type = str,help = "Output name without extension")

	# Default arguments
	parser.add_argument("--path", type = str, default = '/home/jmurga/mkt/201902/rawData/simulations/', help = "Path to output file")

	
	# Parsing common arguments
	args = parser.parse_args()

	output = args.path + '/' + args.output + '.txt'
	regions = pd.DataFrame({'start':0, 'end':args.length}, index=[0])
	regions = regions[['start','end']]
	burnin = 10 * args.ancSize

	# Selecting baseline recipe
	if(args.recipe == 'baseline'):
	
		slimRecipe = Template(open("/home/jmurga/mkt/201902/scripts/slimRecipes/" + args.recipe + '.slim', "r").read())

		mapping = {
			# 'genomicElements' : genomicElements,
			'mutRate' : args.mutRate,
			'length' : int(args.length),
			'recombRate' : args.recombRate,
			'rb' : float(args.rb),
			'sb' : float(args.sb),
			'sd' : float(args.sd),
			'h' : float(args.dominanceCoef),
			'ancSize' : args.ancSize,
			'generations' : args.generations,
			'burnin' : args.burnin,
			'bins' : int(args.bins),
			'binsApply' : int(args.bins)-1,
			'output' : output
		}

		# print(slimRecipe.substitute(mapping))
		
		with NamedTemporaryFile("w") as slim_file:
			print(slimRecipe.substitute(mapping), file= slim_file,flush=True)
			# print(slimRecipe.substitute(mapping))
			# d0 = []
			# d = []
			# trueAlpha = []
			divergenceAndTrueAlpha = []
			listDaf = []

			# Remove directory and create again
			# os.rmdir(args.path + args.output)
			os.mkdir(args.path + args.output)

			for i in range(0,args.replica,1):
				print(i)

				# Opening slim procces and save custom string output in python variable
				slimResults = subprocess.run(["/home/jmurga/mkt/201902/software/SLiM2.5/bin/slim", "-s", str(random.randint(1, 10**13)),slim_file.name],universal_newlines=True,stdout=subprocess.PIPE)
				
				# Parsing string output, we checked position on slim custom printed output and procces each variable taking into account correspondent positions. 
				rawResults = slimResults.stdout.split('\n')

				# Need to extract position [0] on list due to split function return a list based on split pattern. Each line is an element at the list
				rawD0 = float(rawResults[15:16][0].split(':')[1])
				rawD = float(rawResults[16:17][0].split(':')[1])
				rawTrueAlpha = float(rawResults[17:18][0].split(':')[1])
				rawDaf = rawResults[18:]

				rawDaf = [x.split('\t') for x in rawDaf] 
				rawDaf = rawDaf[:-1]
				header = rawDaf[0]
				rawDaf = rawDaf[1:]

				daf = pd.DataFrame(rawDaf,columns=header)

				# Save results in lists based on scenario replicas
				# d0.append(rawD0)
				# d.append(rawD)
				# trueAlpha.append(rawTrueAlpha)
				tmp = pd.DataFrame({'d':rawD,'d0':rawD0,'trueAlpha':rawTrueAlpha},index=[0])
				divergenceAndTrueAlpha.append(tmp)
				listDaf.append(daf)

				tmp.to_csv(args.path + args.output + '/' + args.output + 'div' + str(i)+'.tab',index=False,header=True, sep='\t')

				daf.to_csv(args.path+args.output+'/'+args.output+'daf'+str(i)+'.tab',index=False,header=True, sep='\t')


			# outputDiv = args.path + args.output + '/'
			# outputDaf = args.path + args.output + '/'

			# Save as RData object including all the scenarios
			# saveRdata(divergenceAndTrueAlpha,'div.RData',outputDiv,div)
			# saveRdata(listDaf,'daf.RData',outputDaf,daf)
