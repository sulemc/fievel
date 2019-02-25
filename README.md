# fievel
Insight DE project

## Project Idea 
  Human trafficking in US is on the rise. According to Polaris, a nonprofit working to combat modern-day slavery and human trafficking, there was a 13 percent jump in identified cases from 2016 to 2017. The National Center for Missing and Exploited children says that 1 in 6 children who go missing are trafficked.  
  I will be sourcing from multiple registries of missing people and cross-referencing them with known human trafficing ads in order to provide the appropriate NGOs, Police departments and local municipalites with relevant information for their areas of expertise.
## Tech Stack
  
| Useage           | Tech Chosen  | Reason                                                 |
|------------------|--------------|--------------------------------------------------------|
| File System      | Azure and S3 | Data coming through NGO on Azure (data privacy issues) |
| Ingestion        |              |                                                        |
| Batch Processing |    Spark     |  distributed computing, able to move into streaming    |                                                |
| Data Store       |  MySQL       |structures data, at this point, no need for anything larger|                                      |
| Web Interface    |     Django   |     Built in user handeling, easy display of SQL queries|                                               |
|                  |              |                                                        |


## Data Source
  A national NGO has provided pure HTML copies from sex ad sites. I scraped for Missing Persons 
        2) https://api.missingkids.org/missingkids/servlet/PubCaseSearchServlet?act=usMapSearch&missState=OH (every state)  
  
## Business Value
  $9.5B business. $150-200k/child/year (avg. 4-6 children). 74% are under 25.
  The Department of Defense have characterized human trafficking as the world's fastest growing crime.
  
## MVP
  Central source of truth for missing people, cross referenced with ads.
