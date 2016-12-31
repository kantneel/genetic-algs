import numpy as np
from matplotlib import pyplot as plt
import random 
import math
import sys

# Hyperparameters 
CROSSOVER = 0.7
MUTATION = 0.001
NUM_GENS = 1000
POP_SIZE = 100
EXP_LENGTH = 8

# Digit & Operator Dictionary
directory = {
	"0000" : 0,
	"0001" : 1,
	"0010" : 2,
	"0011" : 3,
	"0100" : 4,
	"0101" : 5,
	"0110" : 6,
	"0111" : 7,
	"1000" : 8,
	"1001" : 9,
	"1010" : "+",
	"1011" : "-",
	"1100" : "*",
	"1101" : "/",
}

# Used for plotting
popFitness = []

def run(target):
	# Begins the algorithm with the target number.
	genepool = []
	individualLength = 4 * EXP_LENGTH
	fitnessScores = []
	for _ in range(POP_SIZE):
		# making the first generation
		newIndividual = ""
		for a in range(individualLength):
			digit = "1" if random.random() > 0.5 else "0"
			newIndividual += digit
		genepool.append(newIndividual)
		fitnessScores.append(fitnessScore(newIndividual, target))
	fitnessScores = normalize(fitnessScores)

	for a in range(1, NUM_GENS):
		print("On round " + str(a))
		nextGenes = []
		nextFitnesses = []
		# loop used for every next generation
		for b in range(POP_SIZE):
			# picking out a new individual for the next generation
			roulette1 = random.random()
			roulette2 = random.random()
			for i in range(len(fitnessScores)):
				if roulette1 <= fitnessScores[i]:
					roulette1 = i
					break
				else:
					roulette1 -= fitnessScores[i]
			for j in range(len(fitnessScores)):
				if roulette2 <= fitnessScores[j]:
					roulette2 = j
					break
				else:
					roulette2 -= fitnessScores[j]

			if random.random() < CROSSOVER:
				digit = math.floor(random.random() * EXP_LENGTH * 4)
				copy1 = genepool[roulette1]
				copy2 = genepool[roulette2]
				nextGenes.append(copy1[:digit] + copy2[digit:individualLength])
				nextScore = fitnessScore(nextGenes[b], target)
				if nextScore is False:
					end(nextGenes[b], target, a, True)
				else:
					nextFitnesses.append(nextScore)
			else: 
				nextGenes.append(genepool[roulette1])
				nextScore = fitnessScore(nextGenes[b], target)
		genepool = list(nextGenes)
		fitnessScores = list(nextFitnesses)
		fitnessScores = normalize(fitnessScores)
	best = 0
	bestInd = -1
	for i in range(POP_SIZE):
		score = fitnessScore(genepool[i], target)
		if score > best:
			best = score
			bestInd = i
	end(genepool[bestInd], target, NUM_GENS, False)


def fitnessScore(individual, target):
	# individual is a string corresponding to one expression
	# note that the order of operations is left to right, not PEMDAS
	total = -1
	lastOperator = False
	for i in range(EXP_LENGTH):
		gene = individual[4 * i : 4 * (i + 1)]
		if not gene in directory:
			continue
		if type(directory[gene]) == int and total == -1:
			total = directory[gene]
			lastOperator = False
		elif type(directory[gene]) == int and lastOperator:
			if lastOperator == "+":
				total += directory[gene]
			elif lastOperator == "-":
				total -= directory[gene]
			elif lastOperator == "*":
				total *= directory[gene]
			elif directory[gene] == 0:
				return 0
			else:
				total /= directory[gene]
			lastOperator = False
		elif type(directory[gene]) == str and (not lastOperator and total > -1):
			lastOperator = directory[gene]
	if target == total:
		return False
	return (1.0 / abs(target - total)) ** 2

def normalize(scores):
	fitnessScores = list(scores)
	total = math.fsum(fitnessScores)
	popFitness.append(total / POP_SIZE)
	for i in range(len(fitnessScores)):
		fitnessScores[i] = fitnessScores[i] / total
	return fitnessScores

def end(individual, target, gens, success):
	# Used for declaring end of session
	if success:
		print("Trial for target value of %s was Successful after %s generations!" % (target, gens))
		print("Successful individual:")
	else:
		print("No successful individuals found for target %s after %s generations." % (target, gens))
		print("Closest individual:")
	
	message = ""
	for i in range(EXP_LENGTH):
		if individual[4 * i : 4 * (i + 1)] not in directory:
			message += " NaN"
		else:
			message += " " + str(directory[individual[4 * i : 4 * (i + 1)]])
	print(message[1:])
	times = np.arange(gens)
	fitnesses = np.asarray(popFitness)
	print(np.size(times), np.size(fitnesses))
	plt.plot(times, fitnesses)
	plt.axis([0, gens, 0, max(popFitness)])
	plt.show()
	sys.exit(1)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Please enter exactly one target number.")
	else:
		run(int(sys.argv[1]))





