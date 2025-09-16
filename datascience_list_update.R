library(tidyverse)

# Students currently on the DATASCIENCESTUDENTS-L listserv
listserv <- read_csv('subscriber-report.csv')

# Students currently enrolled in a Data Science program (anywhere in the University)
bilist <- read_csv('DataEmailsFall2025.csv',locale=locale(encoding='UTF-16'))

# The listserv does a terrible job of rendering emails.  Fix that...
listserv_emails <- listserv |> 
  mutate(email=map(Subscribers, function(x){
    str_split_1(x,' ') |> 
      first()})|> 
      unlist() |> 
      str_to_lower()) |> 
  select(email)

# Students who are not on the listserv (regardless of which email they used)
# Note: email types from BI appear to be either "INT" or "AU"; if either one of
# these show in the listserv, we won't report the student as new to the listserv
new_students <- bilist |>
  pivot_wider(id_cols=AUID, names_from = `Student Email Type`, values_from = `Student Email`) |>
  anti_join( listserv_emails, by=c(INT='email')) |>
  anti_join( listserv_emails, by=c(AU='email')) |>
  filter(!is.na(AUID))

# For those students not on the listserv, report their preferred email address
listserv_adds <- bilist |> 
  filter(AUID %in% new_students$AUID) |>
  filter(`Student Email Type Preferred` == 'Y') |>
  mutate(email=`Student Email`) |>
  select(email)

listserv_adds |>
  write_csv('listserv_adds.csv',col_names = FALSE)
