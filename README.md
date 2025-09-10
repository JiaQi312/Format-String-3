# Format-String-3
My writeup on the picoCTF challenge: Format-String-3

## My Process

I originally had no clue how to solve this problem, since there was not an obvious win function. ChatGPT was very useful here, explaining to me the concept of the challenge and what I would have to do. This allowed me to start writing the script, but it was not working, so I had ChatGPT look at it again and tell me what may be wrong with it. I copied its version of the script, which was very similar to mine. But, there was one crucial thing I was missing, which was the interactive(). 

## Rundown

This is a Ret2Libc problem. The goal is to call system() on the string "/bin/sh", which creates a shell that will have the flag. 

The "/bin/sh" string is given as an argument for puts, which prints it out. To call puts, the binary has a table called the Global Offset Table (GOT), which has an entry for puts. This entry holds the current address of puts in libc. So, if you can figure out the address of system() in libc, you can overwrite the GOT entry for puts and replace it with system, in order to create your shell. 

The address for puts can be printed out from the GOT within the binary. To get the address of system, you need several things. 1: The version of libc used by the challenge. 2: The offset of setvbuf for that version. 3: The offset of system for that version. You are provided the libc, so that solves one. There is also a variety of ways to obtain the offset of setvbuf and system. 

Now, the challenge gives you the current address of setvbuf. This address changes on each run of the challenge because the base address of libc is different each time. However, the offset, or the distance setvbuf is from the base, stays the same. 

By subtracting the setvbuf offset from the address you are given, you get the base address of libc. By adding system's offset, you now have the current address of system. With the format string explot, utilizing %n, you want to replace the entry of puts within the GOT with the current address for system. If all goes well, the shell will spawn successfully. 

## What I Learned

ChatGPT is SUPER useful. It taught me: 
- system("/bin/sh") spawns a shell
- you need interactive() in order to work with the shell
- how to complete the challenge in general

However, it is important to me not to overrely on ChatGPT. To this degree, I made sure that I can write the script and that I understood the code ChatGPT provided, which means I learned something substantial from the challenge. 