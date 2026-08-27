# Attaching a New EBS Volume to a Linux EC2 Instance

## Step 0: Check Current Disk Layout

Before attaching, check what's currently visible to the instance.

```bash
df -h
```

```
Filesystem        Size  Used Avail Use% Mounted on
devtmpfs          420M     0  420M   0% /dev
tmpfs             457M     0  457M   0% /dev/shm
tmpfs             183M  448K  183M   1% /run
efivarfs          128K  2.7K  121K   3% /sys/firmware/efi/efivars
/dev/nvme0n1p1    8.0G  1.8G  6.2G  22% /
tmpfs             457M     0  457M   0% /tmp
/dev/nvme0n1p128   10M  1.3M  8.7M  13% /boot/efi
tmpfs              92M     0   92M   0% /run/user/1000
```

```bash
lsblk
```

```
NAME          MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
nvme0n1       259:0    0   8G  0 disk
├─nvme0n1p1   259:1    0   8G  0 part /
├─nvme0n1p127 259:2    0   1M  0 part
└─nvme0n1p128 259:3    0  10M  0 part /boot/efi
nvme1n1       259:4    0   2G  0 disk
```

`nvme1n1` is the new 2GB EBS volume — it is already attached at the instance level (from the AWS console) and visible to the OS, but has no filesystem and is not mounted yet.

## Step 1: Confirm the New Disk Has No Filesystem

```bash
sudo file -s /dev/nvme1n1
```

- If it returns just `/dev/nvme1n1: data` (no filesystem type listed) — the disk is blank and safe to format.
- If it shows something like `ext4 filesystem data` — it already has data on it. Don't format; skip to Step 3.

## Step 2: Create a Filesystem on the Volume

Format the whole disk (not a partition, since there isn't one yet):

```bash
sudo mkfs -t xfs /dev/nvme1n1
```

XFS is the Amazon Linux default. Use ext4 instead if you prefer it:

```bash
sudo mkfs -t ext4 /dev/nvme1n1
```

## Step 3: Create a Mount Point

```bash
sudo mkdir /data
```

Use whatever path makes sense for your use case (`/mnt/data`, `/opt/appdata`, etc.).

## Step 4: Mount the Volume

```bash
sudo mount /dev/nvme1n1 /data
```

Verify with:

```bash
df -h
```

You should now see `/dev/nvme1n1` mounted at `/data` with about 2GB available.

## Step 5: Get the Volume's UUID

```bash
sudo blkid /dev/nvme1n1
```

Copy the UUID value shown. Use this instead of the device name in the next step, since device names like `/dev/nvme1n1` aren't guaranteed to stay consistent across reboots.

## Step 6: Make the Mount Persist Across Reboots

Back up fstab first:

```bash
sudo cp /etc/fstab /etc/fstab.orig
```

Edit it:

```bash
sudo vi /etc/fstab
```

Add a line like:

```
UUID=xxxx-xxxx-xxxx  /data  xfs  defaults,nofail  0  2
```

Use `ext4` instead of `xfs` if that's what you formatted with. The `nofail` option is important — without it, if the volume is ever detached later, the instance could fail to boot.

## Step 7: Test the fstab Entry Before Rebooting

```bash
sudo umount /data
sudo mount -a
```

If it remounts cleanly with no errors, the fstab entry is correct and the volume will come back mounted after a reboot. If you get an error, fix the fstab line before rebooting.
