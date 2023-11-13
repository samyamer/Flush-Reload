# Replication of Flush+Reload

# Takeaways from paper
    - Don't forget to serialize instructions
    - Long keys are easier
    - Use mmap to share the binary with the process (GnuGPG)
    - Need to serialize instructions


# Calibration of threshold

The threshold for HIT/MISS is system dependent so we need to calibrate. I used the THIS repo [link]

The way it works is by counting the nunber of times a HIT/MISS took x cycles. The threshold is somewhere between the maximum time it took for a hit and the minimum time it took for a miss. As long as the difference is big we are in the clear.

Looking at the historgam data I can see that there are no misses that take less than 3 digit cycles, while the fastest hit took 56 cycles. Looking at the distribution we can determine a reasonable threshold.

# Finding addresses to probe
GnuPG compiles with the -02 flags, which shuffles things a bit on compilation. So I had to inspect the objdump of the excutable to fidn the functions I needed. The offsets that appear in the objdump have an extra 0x100000000 (due to VM stuff), so to get the offset from the pointer mmap returns I subtract 0x100000000 from the offset in the objdump. I confirm the address is correct by printing the bytes and comparing with the objdump.


# Setup
Must use gcc <10 make will error
Download GPG
    wget https://gnupg.org/ftp/gcrypt/gnupg/gnupg-1.4.13.tar.gz

    tar -xvf gnupg-1.4.13.tar.gz
    cd gnupg-1.4.13
    ./configure
    make
    sudo make install
# Worth Noting
There is a pattern in the spy output that shows a block of 1/0s followed by a continous block of 0s followed by a block of 1/0s. I speculate that this is in the time window where gpg is switching from d_p/d_q:

# Validation of Attack
Here I present this question, how many bits of d_p/d_q should the spy retrieve to prove that it wasn't a fluke? After all, if it outputs all 0s then it will have a common substring with d_p/d_q of at least length 1.

In a string of m randomly generated 1s and 0 (spy output), what is the probability of occurence of an n-long substring (longest common substring between spy and d_p/d_q)?

There are (m-n+1) n-long substrings (sliding window of size n). This means that there are (m-n+1) trials. For simplicity, I assume the trials are independent, which they are not, since there is overlap. However, this assumption leads to an overestimation of the probability, which is good in our scenario.
The probability of an n-long substring is 2^{-n}. We can model the probability of a spy having at least 1 success (a single common substring of size n) as a binomial distribution with a probability of success being 2^-n and (m-n+1) trials.

Let X denote the number of successes. Let F denote P(X>=1).F essentialy denotes the probability of a spy being a fluke.
F=P(X>=1) = 1 - P(X=0) = 1-(1-2^-n)\*\*(m-n+1)

This means that the probability of an n-long substring occuring in an m-long string is 1-(1-2^-n)\*\*(m-n+1)

A perfect spy outputs the exact length of d_p or d_q with all the correct bits. n is equal to the length of d_p/d_q, since this is the longest common substring between the spy's output and d_p/d_q. Therefore m and n are equal, hence,
F = 1-(1^2-n) =2^-n, where n is the length of d_p/d_q. Since d_p/d_q has a length of 4095, F =  2^-4095 for this perfect spy.
