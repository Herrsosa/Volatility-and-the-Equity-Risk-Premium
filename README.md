# Volatility-and-the-Equity-Risk-Premium

Code written for the empirical part of my master thesis "Volatility and the Equity Risk Premium". 
The code constructs a volatility linked real time index of the equity risk premium and its term structure according to "What is 
the Expected Return on the Market?" (Martin, 2017). Further, probabilities of a 20% market decline implied by option prices are calculated.

# Code
- SVIXConstruction.py - Given European S&P 500 option price data, an index of the equity risk premium (called SVIX) is constructed at 5 
                        maturities. 
- CrashProbabilities.py - Given European S&P 500 put option price data, the implied probability of a 20% market correction is calculated. 
- TermStructure.py - Given the SVIX index, a term strucutre of equity risk premia is constructed. 

# Links
[What is the Expected Return on the Market? (Martin, 2017) available under.](http://personal.lse.ac.uk/martiniw/) 













