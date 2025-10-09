# Pantry Pilot - Testing

## Validation Testing

### HTML Validation
**[W3C Markup Validation Service](https://validator.w3.org/)** was used to validate the HTML on all pages of the site.
HTML was checked by running the deployed page url through the validator.

<details>
    <summary>Expand to view the results</summary>

| Page | Result | Evidence |
|------|--------|----------|
| Home Page (Dashboard) - Unauthenticated | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/dashboard_unauthenticated_page.png) |
| Home Page (Dashboard) - Authenticated | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/dashboard_unauthenticated_page.png) |
| Sign Up Page | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/signup_page.png) |
| Sign In Page | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/signin_page.png) |
| Sign Out Page | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/signout_page.png)<sup>1</sup> |
| Pantry Management | ✅ Pass | No errors or warnings found in HTML validation |
| Recipe Discovery | ✅ Pass | No errors or warnings found in HTML validation |
| Recipe Detail | ✅ Pass | No errors or warnings found in HTML validation |
| Meal Planning | ✅ Pass | No errors or warnings found in HTML validation |
| Shopping Lists | ✅ Pass | No errors or warnings found in HTML validation |

Note:
- <sup>1</sup> Validation by deployed webpage's source code instead of URL beacuse the validator kept redirecting to home page for the url. 
</details>