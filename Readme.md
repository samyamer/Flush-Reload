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

