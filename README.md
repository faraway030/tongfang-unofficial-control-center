# TUCC - Tongfang-Unofficial-Control-Center
## Description
Inspired by [aucc](https://github.com/rodgomesc/avell-unofficial-control-center).

This is a linux driver to control keyboard backlight of laptops based on a <b>Tongfang GM7MP7P</b> barebone like <b>PCSpecialist Vyper 17"</b> or the <b>Eluktronics MAX-17</b>.
Even if it's also an <b>Integrated Technology Express ITE Device(8291) Rev 0.03</b>, it's a completely different keyboard, which unfortunately doesn't work with aucc.


## Compatibility
With `sudo hwinfo --keyboard` check your keyboard model.<br>

It should show the following:
```
...
Vendor: usb 0x048d "Integrated Technology Express, Inc."
Device: usb 0xce00 "ITE Device(8291)"
...
```
### Known compatible devices
- PCSpecialist Vyper 17"
- Eluktronics MAX-17

Write me an email if you found some more.

## Project status
### Working
- Set plain colors
- Set brightness
- Control all 4 areas seperately
- Disable backlight

### To do
- Set pre-defined styles
- Analyze how to program the startup mode (hex-dump shows no difference to normal mode)
- Control the light bar
- Build a package

## Usage
### Plain colors
#### Colors currently availabe: `white`, `red`, `blue`, `teal`, `green`, `yellow`, `orange`, `gold`, `cyan`, `pink`
#### Brightness options are: `1`, `2`, `3`, `4`
#### Area options are: `1`, `2`, `3`, `4`
<br>
<b>To set green color on all areas with max brightness:</b>

```bash
sudo main.py -c green -b 4
```

<b>To set blue color on only the first area:</b>

```bash
sudo main.py -c blue -a 1
```

If no brightness parameter -b is provided, max brightness 4 is applied.<br>
If no area parameter -a is provided, color is applied to all areas.

<b> To disable the keyboard backlight:</b>

```bash
sudo main.py -d
```

## Contributions
Contributions of any kind are welcome.

## Donate :coffee: :heart:

This is a project I develop in my free time. If you use `tongfang-unofficial-control-center` or simply like the project and want to help please consider [donating a coffee](https://www.buymeacoffee.com/teyifigoda).