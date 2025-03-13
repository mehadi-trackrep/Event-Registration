#1) For Generating SMS text:-

=ARRAYFORMULA(IF((A2:A <> "") * (B2:B <> ""),
"আপনার রেজিস্ট্রেশনটি সফলভাবে সম্পন্ন হয়েছে।" & CHAR(10) &
"নাম - " & C2:C & CHAR(10) &
"বাবার নাম - " & D2:D & CHAR(10) &
"মায়ের নাম - " & E2:E & CHAR(10) &
"গ্রাম - " & F2:F & CHAR(10) &
"ব্যাচ - " & B2:B,
""))


#2) Make new sheet showing batch wise sorted data:-

=SORT(IMPORTRANGE("https://docs.google.com/spreadsheets/d/....", "MainData!C2:Q"), 3, TRUE)

N.B. The above link is the MainData sheet link (main database got from the tally integration).
The link is upto '/edit'.

#3) Again same thing of 2):-

Sheet1: =SORT(IMPORTRANGE("https://docs.google.com/spreadsheets/d/...", "MainData!A2:AC"), 5, TRUE)
BasicData: =QUERY(Sheet1!A:AC,"select C, E, F, H, I, J, K, L, G, N, O, R, V, AC")