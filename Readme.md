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

# Setup
Download GPG
    wget https://gnupg.org/ftp/gcrypt/gnupg/gnupg-1.4.13.tar.gz
    
    tar -xvf gnupg-1.4.13.tag.gz
    cd gnupg-1.4.13
    ./configure
    make
    sudo make install