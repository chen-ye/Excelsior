### New files from Adam 8/6/14  all_grouped_medians.csv is for automated track data from Chen Ye's program with every instantaneous velocity (a derivitive across 1/15 second intervals of dY/dT for about 20-25 seconds).  The excel file is the manual tracked file from Adam, some rows are for 0, 3, 6, 9 cm.  Pixels go in reverse order so 0s have larger Y value sfo rhte pixel count.  Ecel file velocities need to be sclaed differently due to camera distance.  Young scalar = 0.02868. old scalar = 0.0282.  last column is this multiplied by Dy_abs value in excel file.

velauto <- read.csv("/Users/davidrand/Documents/Grants/HHMI Undergraduate/2014 Project/HHMIclimbing/all_grouped_medians.csv", colClasses=c(rep('factor',5), rep('numeric',15)))
head(velauto)
plot(velauto$Velo_mean_cm_sec, velauto$Velo_median_cm_sec)
summary(velauto)
velpos <- velauto[ which(velauto$Velo_mean_cm_sec > 0), ]
velpos2 <- velauto[ which(velauto$Velo_mean_cm_sec > 0 | velauto$Velo_median_cm_sec > 0), ]
velpos3 <- velauto[ which(velauto$Velo_mean_cm_sec > 0 & velauto$Velo_median_cm_sec > 0), ]

velpostrim <- velauto[ which(velauto$Velo_mean_cm_sec > 0 & velauto$Velo_median_cm_sec > 0 & velauto$Velo_mean_cm_sec < 2), ]

plot(velpos$Velo_mean_cm_sec, velpos$Velo_median_cm_sec, col=velauto$Diet)
plot(velpos3$Velo_mean_cm_sec, velpos3$Velo_median_cm_sec, col=velpos3$Diet)

velaov <- aov(Velo_median_cm_sec ~ Age*Nuclear*Mito*Diet, velpos)
summary(velaov)

veltrimaov <- aov(Velo_median_cm_sec ~ Age*Nuclear*Mito*Diet, velpostrim)
summary(veltrimaov)


boxplot(Velo_median_cm_sec ~ Age*Nuclear*Mito, data=velpos)
boxplot(Velo_mean_cm_sec ~ Age*Mito, data=velpos)

plot(velpostrim$Velo_mean_cm_sec, velpostrim$Velo_median_cm_sec, col=velpostrim$Age)
velaovtrim <- aov(Velo_median_cm_sec ~ Age*Nuclear*Mito*Diet, velpostrim)
summary(velaovtrim)

boxplot(Velo_median_cm_sec ~ Age*Nuclear*Mito, data=velpostrim, las=2)
boxplot(Velo_mean_cm_sec ~ Age*Mito, data=velpostrim)

summary(velpostrim)



### Manual data analyzed here
velman <- read.csv("/Users/davidrand/Documents/Grants/HHMI Undergraduate/2014 Project/HHMIclimbing/Manual_Fly_Tracks.csv", colClasses=c(rep('factor',9), rep('numeric',4)))
head(velman)
velman3 <- velman[ which(velman$Time..sec. == "3"), ]
velman6 <- velman[ which(velman$Time..sec. == "6"), ]
velman9 <- velman[ which(velman$Time..sec. == "9"), ]

plot(velauto$Velo_mean_cm_sec, velauto$Velo_median_cm_sec)
summary(velauto)

velman3aov <- aov(veloscaled ~ Age*Nuclear*Mito*Diet, velman3)
summary(velman3aov)

velman6aov <- aov(veloscaled ~ Age*Nuclear*Mito*Diet, velman6)
summary(velman6aov)

velman9aov <- aov(veloscaled ~ Age*Nuclear*Mito*Diet, velman9)
summary(velman9aov)

boxplot(veloscaled ~ Age*Nuclear*Mito, data=velman, las=2, frame=T, xlab="Age.Nuclear.Mito", ylab="Climbing velocity(cm/sec)", col=(c("green3", "green3", "red", "red", "thistle", "thistle", "steelblue1", "steelblue1", "orchid", "orchid", "turquoise4", "turquoise4", "white", "white", "yellow", "yellow", "orange", "orange", "rosybrown1", "rosybrown1", "darkseagreen2", "darkseagreen2", "gray60", "gray60")), names=c("Old 15B", "Young 15B", "Old 15C", "Young 15C", "Old 15G", "Young 15G", "Old 15I", "Young 15I", "Old 19B", "Young 19B", "Old 19C", "Young 19C", "Old 19G", "Young 19G", "Old 19I", "Young 19I", "Old 3B", "Young 3B", "Old 3C", "Young 3C", "Old 3G", "Young 3G", "Old 3I", "Young 3I"))
boxplot(veloscaled ~ Mito+Nuclear+Age, data=velman3, las=2, xlab="Age.Nuclear.Mito", ylab="Climbing velocity(cm/sec)", col=(c("green3", "green3", "red", "red", "thistle", "thistle", "steelblue1", "steelblue1", "orchid", "orchid", "turquoise4", "turquoise4", "white", "white", "yellow", "yellow", "orange", "orange", "rosybrown1", "rosybrown1", "darkseagreen2", "darkseagreen2", "gray60", "gray60")), names=c("Old 15B", "Young 15B", "Old 15C", "Young 15C", "Old 15G", "Young 15G", "Old 15I", "Young 15I", "Old 19B", "Young 19B", "Old 19C", "Young 19C", "Old 19G", "Young 19G", "Old 19I", "Young 19I", "Old 3B", "Young 3B", "Old 3C", "Young 3C", "Old 3G", "Young 3G", "Old 3I", "Young 3I"))
boxplot(veloscaled ~ Age*Nuclear*Mito, data=velman9, las=2, frame=T, xlab="Age.Nuclear.Mito", ylab="Climbing velocity(cm/sec)", main="Climbing speed at 9cm", col=(c("green3", "green3", "red", "red", "thistle", "thistle", "steelblue1", "steelblue1", "orchid", "orchid", "turquoise4", "turquoise4", "white", "white", "yellow", "yellow", "orange", "orange", "rosybrown1", "rosybrown1", "darkseagreen2", "darkseagreen2", "gray60", "gray60")), names=c("O 15B", "Y 15B", "O 15C", "Y 15C", "O 15G", "Y 15G", "O 15I", "Y 15I", "O 19B", "Y 19B", "O 19C", "Y 19C", "O 19G", "Y 19G", "O 19I", "Y 19I", "O 3B", "Y 3B", "O 3C", "Y 3C", "O 3G", "Y 3G", "O 3I", "Y 3I"))
plot(velman6$veloscaled, velman9$veloscaled)

#stack overflow answer to moving  x lable position on box plot
boxplot(c(1:12)~c(rep("1",6),rep("2",6)),at=c(1,2), col=c(0,"grey"),las=1,xaxt="n") 
axis(1,at=c(1,2),adj=1,labels=c("Salix Scrub","Tall Forb")) 
axis(1,at=c(1,2),adj=1,padj=0.5,labels=c("Salix\nScrub","Tall\nForb")) 




# check dimensions of adams monster file from flash drive read.
test<- read.csv("/Volumes/Metabolon/Derived_young_concatenated.csv")
test5k<-test[1:5000, ]
plot(test5k$Velocity, test5k$Velocity_Median)

grouped <- read.csv("/Volumes/Metabolon/grouped_median_velocity.csv")
head(grouped)
plot(grouped$Velocity, grouped$Velocity_Median, col=grouped$Age)

# 8/4/14 files and email from Adam These files contain the velocities for the flies from the time indicated to time 0, we can also segment out how well the flies climb in between the specific intervals, which may also be cool since there is a variable decline in climbing ability that seems to increase with the length of the assay

# Reading in csv files...modify your path accordingly
t3=read.csv("~/Desktop/Fly Tracking/Manual Flylapse Images/Manual_tracks_T3.csv",colClasses=c(rep('factor',9), rep('numeric',4)))
t6=read.csv("~/Desktop/Fly Tracking/Manual Flylapse Images/Manual_tracks_T6.csv",colClasses=c(rep('factor',9), rep('numeric',4)))
t9=read.csv("~/Desktop/Fly Tracking/Manual Flylapse Images/Manual_tracks_T9.csv",colClasses=c(rep('factor',9), rep('numeric',4)))


# Analysis of variance using velocity in the y-direction exclusively. Comparing the interaction between Age, Nuclear, Mito, and Diet types
aov_3<-aov(t3$Dy~t3$Age*t3$Nuclear*t3$Mito*t3$Diet)
aov_6<-aov(t6$Dy~t6$Age*t6$Nuclear*t6$Mito*t6$Diet)
aov_9<-aov(t9$Dy~t9$Age*t9$Nuclear*t9$Mito*t9$Diet)

# Displays the stats
summary(aov_3)
summary(aov_6)
summary(aov_9)

# ANOVA for same parameters as above. This function is different? in that it uses a linear model to look at how related everything is
anova_3=lm(t3$Dy~t3$Age*t3$Nuclear*t3$Mito*t3$Diet)
anova_6=lm(t6$Dy~t6$Age*t6$Nuclear*t6$Mito*t6$Diet)
anova_9=lm(t9$Dy~t9$Age*t9$Nuclear*t9$Mito*t9$Diet)

# Displays the stats
summary(anova_3)
summary(anova_6)
summary(anova_9)
# Note: interesting how "Mito I" is such a troublemaker...and that gets more pronounced with length of the assay as well
