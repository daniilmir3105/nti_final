from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl
from statistics import mean

session = WolframLanguageSession()

sample = session.evaluate(wl.RandomVariate(wl.NormalDistribution(0,1), 1e6))

print(sample[:5])

session.evaluate(wl.Mean(sample))

mean(sample)