# pge-ebok
Showing PGE energy bill. (Polska Grupa Energetyczna)

## Installation
### HACS (Recommended)
1. Install and configure [HACS](https://hacs.xyz/).
2. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) using:
```
[https://github.com/arni077r/pge-ebok/]
```
3. In HACS, search for **"PGE ebok"**, install the integration.
4. Restart Home Assistant.


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





# Legal notice
This is a personal project and isn't in any way affiliated with, sponsored or endorsed by PGE.
All product names, trademarks and registered trademarks in (the images in) this repository, are property of their respective owners. All images in this repository are used by the project for identification purposes only.

The data source for this integration is https://ebok.gkpge.pl/

The author of this project categorically rejects any and all responsibility for the data that were presented by the integration.

Anything else? Post a [question.](https://github.com/arni077r/pge-ebok/issues/new)
