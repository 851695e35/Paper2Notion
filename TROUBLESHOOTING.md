# GS2Notion - Troubleshooting Guide

## Network Connectivity Issue

Your system has intermittent connectivity to Google APIs. Here are solutions in order of ease:

### Solution 1: Use a VPN (Easiest)
If you're behind a corporate firewall, using a VPN will bypass it:
1. Download a VPN (e.g., ProtonVPN, NordVPN, Windscribe - free options available)
2. Connect to the VPN
3. Run the automation script

### Solution 2: Use a Different Network
Try running from:
- Home WiFi (if different from current network)
- Mobile hotspot from your phone
- Public WiFi (coffee shop, library)

This will help identify if it's a network-specific issue.

### Solution 3: Contact Your Network Administrator
If you're on a corporate network, ask your IT department to:
- Whitelist googleapis.com
- Allow outbound HTTPS connections to Google APIs
- Check if there's a proxy that needs to be configured

### Solution 4: Use Cloud Deployment (Advanced)
Deploy the automation to a cloud server (AWS, Google Cloud, Heroku) that has unrestricted internet access. The script will run there continuously.

### Solution 5: Alternative: Use Google Sheets as Input
Instead of polling Gmail, we can:
1. Create a Google Sheet with paper titles
2. The script reads from the sheet
3. Processes and writes results to Notion

This avoids Gmail API connectivity issues entirely.

---

## Quick Test

Try this to verify the issue:
```bash
python diagnose_network.py
```

If you see [FAIL] on TCP/SSL tests, it's a firewall/network issue.

---

## Recommended Next Steps

1. **Try a VPN first** - quickest solution
2. **If that works**, the automation is ready to use
3. **If VPN doesn't help**, try a different network
4. **If still failing**, contact your network admin or use cloud deployment

Let me know which solution you'd like to try!
