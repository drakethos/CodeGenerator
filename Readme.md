# CodeGen 
## By Derrick Kamphaus
### Changelog
Version 1.0:
 - initial Upload 4/18/2023

Version 1.1a 
 - added header and footer logic 0 4/18/2023

## Todo:
**Cleanup**: technical refactoring several reused items into their own functions for better reusibility and cleaner code.

**New Tags**:
Wrap around the repetitive code for a full document, IE one time only code at top and bottom then repeat the code in the
middle

**<$header>** - Add a tag that will be used as the beginning of template ending with </$header>

**<$footer>** - Add a tag that will be at the end of the template ending with </$footer>

**$break** - Add a tag that will effectively treat the template as starting over, for count and any data in cases where
repetition is occurs with slight variation.