# pge-ebok
Showing PGE energy bill


## Manual Configuration
Sample configuration

```yaml
sensor:
  - platform: pge_ebok
    username: YOUR USERNAME
    password: YOUR PASSWORD
```
It is recommended to confiure the sensor through the UI.

## Through the interface
1) Navigate to Settings > Devices & Services and then click Add Integration
2) Search for PGE ebok
3) Enter your credentials (e-mail and password)

## Technical Details

The sensor uses API from https://ebok.gkpge.pl 
and is particularly focused on the bill reading endpoint. 

The data is refreshed every 24 hours or on the sensor startup.
