# VPS Access Information

**IP Address:** 23.95.148.204
**Username:** root (likely, based on workspace path)
**Workspace:** /root/.openclaw/workspace/research/bathroom-products/

## SSH Access

### From Local Terminal
```bash
ssh root@23.95.148.204
```

### With SSH Key (if configured)
```bash
ssh -i ~/.ssh/your_key.pem root@23.95.148.204
```

### With Specific Port (if not default 22)
```bash
ssh -p [PORT] root@23.95.148.204
```

### From Windows (PowerShell)
```powershell
ssh root@23.95.148.204
```

### From Windows (PuTTY)
- Host: 23.95.148.204
- Port: 22 (or your custom port)
- Username: root
- Password: [your VPS password]

## File Transfer (SCP)

### Upload Files to VPS
```bash
# From local machine
scp /path/to/local-file.csv root@23.95.148.204:/root/.openclaw/workspace/research/bathroom-products/

# Upload directory
scp -r /path/to/local-dir/ root@23.95.148.204:/root/.openclaw/workspace/research/bathroom-products/
```

### Download Files from VPS
```bash
# From local machine
scp root@23.95.148.204:/root/.openclaw/workspace/research/bathroom-products/product-catalog-refined.csv ./
```

### With SCP from Windows
```bash
pscp root@23.95.148.204:/root/.openclaw/workspace/research/bathroom-products/*.csv C:\Users\peter\Downloads\
```

## SFTP (FileZilla, WinSCP, etc.)

### FileZilla
- Protocol: SFTP
- Host: 23.95.148.204
- Port: 22
- User: root
- Password: [your password]

### WinSCP
- Host name: 23.95.148.204
- Port number: 22
- User name: root
- Password: [your password]
- File protocol: SFTP

## Quick Commands Once Connected

### Navigate to workspace
```bash
cd /root/.openclaw/workspace/research/bathroom-products/
```

### List files
```bash
ls -la
```

### View CSV content
```bash
head -20 product-catalog-refined.csv
```

### Check database
```bash
psql -U postgresql://postgres:***@***.supabase.co -c "SELECT COUNT(*) FROM products;"
```

## Security Notes

⚠️ **IMPORTANT:**
- Never share your VPS password publicly
- Use SSH keys instead of passwords when possible
- Consider changing default SSH port from 22 to custom port
- Enable firewall (ufw) to restrict access
- Keep SSH key files secure (chmod 600)

## Troubleshooting

### Connection Refused
- Check SSH port: `ssh -p 2222 root@23.95.148.204`
- Verify firewall rules
- Check if SSH service running: `systemctl status sshd`

### Permission Denied
- Verify username (might not be root)
- Check password/SSH key
- Ensure user has sudo access if needed

### Connection Timeout
- Check if VPS is running
- Verify network connectivity
- Check firewall rules
