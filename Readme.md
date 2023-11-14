# Replication of Flush+Reload


# Results
I measured success using the length of the longest common substring(LCS) bewteen the spy's output and d_p/d_q. I also calculate the probability of getting this LCS by pure luck.
The best result I was able to achieve is a LCS of length 29 with d_q, with a probability of being pure luck of $9.26\*10^{-6}$. GPG signature was doing signatures in a loop in the background, so it is likely that the spy witnessed multiple signatures.
See next section for details.

# Validation of Attack
Here I find a way to calculate the probability that the spy's output was just a lucky guess.

How many bits of d_p/d_q should the spy retrieve to prove that it wasn't a fluke? After all, if it outputs all 0s then it will have a common substring with d_p/d_q of at least length 1. I formulate this problem as a binomial distribution.

In a string of m randomly generated 1s and 0 (spy output), what is the probability of occurence of an n-long substring (longest common substring between spy and d_p/d_q)?

There are (m-n+1) n-long substrings (sliding window of size n). This means that there are (m-n+1) trials. For simplicity, I assume the trials are independent, which they are not, since there is overlap. However, this assumption leads to an overestimation of the probability, which is good in our scenario.
The probability of an n-long substring is $2^{-n}$. We can model the probability of a spy having at least 1 success (a single common substring of size n) as a binomial distribution with a probability of success being $2^{-n}$ and (m-n+1) trials.

Let X denote the number of successes. Let F denote P(X>=1).F essentialy denotes the probability of a spy being a fluke.
$F=P(X>=1) = 1 - P(X=0) = 1-(1-2^{-n})^{(m-n+1)}$

This means that the probability of an n-long substring randomly occuring in an m-long string is $1-(1-2^-n)\*\*(m-n+1)$

A perfect spy outputs the exact length of d_p or d_q with all the correct bits. n is equal to the length of d_p/d_q, since this is the longest common substring between the spy's output and d_p/d_q. Therefore m and n are equal, hence,
$F = 1-(1-2^{-n}) =2^{-n}$, where n is the length of d_p/d_q. Since d_p/d_q has a length of 4095, $F =  2^{-4095}$ for this perfect spy.

In the result I obtained the spy had an output of 5000 bits and a LCS of length 29, which means $F = 9.26\*10^{-6}$.

# Sanity Checks
To make sure I wasn't just seeing things I did two sanity checks.
1. Spy running without any GPG signatures running --> output was all 0s as expected
2. Looked at hit times to make sure these weren't just values on the border of the threshold --> Hit times observed were less than 150.

# Calibration of threshold
I ran the attack on an Intel i3-4005U CPU, which is an Ivy Bridge architecture.

The threshold for HIT/MISS is system dependent so we need to calibrate. I used the this(https://github.com/IAIK/flush_flush). The way it works is by counting the nunber of times a HIT/MISS took x cycles. Looking at the time distribution of hits I chose 200 cycles as the threshold.


# Finding addresses to probe
GnuPG compiles with the -02 flags, which shuffles things a bit on compilation. So I had to inspect the objdump of the excutable to fidn the functions I needed. I probed addresses right before the return instructions in the following functions: mpih_sqr_n_basecase, mpihelp_divrem,mpihelp_mul_karatsuba_case. (See screenshot of gpp code below).

# Busy Wait Cycles
Probably the least documented aspect of this attack. How many cycles should the attacker wait before it reloads? If it does not wait long enough it will mostly miss. If it waits too long it will mostly hit. Through trial and error I found that 400 iterations of a nop was the best.

# References
[1] Yarom, Y., & Falkner, K. (2014). {FLUSH+ RELOAD}: A high resolution, low noise, l3 cache {Side-Channel} attack. In 23rd USENIX security symposium (USENIX security 14) (pp. 719-732)  
[2] Ge, Daniel, & Mally, David, & Meyer, Nicholar.PLUNGER: Reproducing FLUSH+RELOAD: A High-Resolution, Low-Latency Side Channel Attack On GnuPG[https://github.com/DanGe42/flush-reload/releases/tag/cis-700-submission]
# GPG Code Branching on Secret
![alt text](https://github.com/samyamer/Flush-Reload/blob/master/GPG-Code.png)

