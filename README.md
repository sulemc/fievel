# fievel
Insight DE project

## Project Idea 
  Human trafficking in US is on the rise. According to Polaris, a nonprofit working to combat modern-day slavery and human trafficking, there was a 13 percent jump in identified cases from 2016 to 2017. The National Center for Missing and Exploited children says that 1 in 6 children who go missing are trafficked.
  I will be sourcing from multiple registries of missing people and cross-referencing them with known human trafficing ads in order to provide the appropriate NGOs, Police departments and local municipalites with relevant information for their areas of expertise.
## Tech Stack
  
## Data Source
  A national NGO has provided flagged human trafficking ads. I will be scraping from:  
        1. https://www.fbi.gov/wanted/kidnap
        2. https://api.missingkids.org/missingkids/servlet/PubCaseSearchServlet?act=usMapSearch&missState=OH (every state)
        3. http://www.pollyklaas.org/ . 
      As well as state websites and municipalites so as to ensure the most complete source of truth for missing persons
     
## Engineering Challenge
  There are many layers to this project which add complexity
  1) Scraping from multiple sources to create a central source of truth for missing persons
  2) Checking known ads (with their use of coded terms) to create a pool of posssible missing persons the victim could be
  3) Pending the success of the DS team, use their model to identify more ads, actively retrain the model
  4) Source information to the appropriate authorities
  
## Business Value
  $9.5B business. $150-200k/child/year (avg. 4-6 children). 74% are under 25.
  The Department of Defense have characterized human trafficking as the world's fastest growing crime.
  If we can help identify victims and perpetrators faster and get that information to authorities, perhaps we can help.
  
## MVP
  Central source of truth for missing people, cross referenced with known ads.
## Stretch Goals
  Expand into checking reddit and twitter for the coded language used in the ads and see if we can identify trafficking that's happening on these platforms (again cross referencing with the missing persons)
