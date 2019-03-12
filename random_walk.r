library(ggplot2)
library(reshape2)
library(showtext)

font_add('CMUSerif-Roman', paste(Sys.getenv('HOME'), 'Library/Fonts/cmunrm.otf', sep='/'))
font_add('CMUSerif-Italic', paste(Sys.getenv('HOME'), 'Library/Fonts/cmunti.otf', sep='/'))

df1 <- data.frame(
  t = seq(0, 50-1, 5),
  w = cumsum(c(0, sample(c(-1, 1), 10-1, replace=TRUE))))
df2 <- data.frame(
  t = seq(0, 50-1, 2),
  w = cumsum(c(0, sample(c(-1, 1), 25-1, replace=TRUE))))
df3 <- data.frame(
  t = seq(0, 50-1, 1),
  w = cumsum(c(0, sample(c(-1, 1), 50-1, replace=TRUE))))

df1.melt <- melt(df1[, c('t', 'w')], id='t')
df2.melt <- melt(df2[, c('t', 'w')], id='t')
df3.melt <- melt(df3[, c('t', 'w')], id='t')

df1.melt[, 'variable'] <- '10'
df2.melt[, 'variable'] <- '25'
df3.melt[, 'variable'] <- '50'

df <- rbind(df1.melt, df2.melt, df3.melt)

gg <- ggplot(data = df, aes(x = t, y = value, colour = variable)) +
  geom_line() +
  geom_point() +
  labs(color='Number of Steps') +
  xlab('t') +
  ylab('W(t)') +
  coord_cartesian(expand = FALSE, clip = 'off') +
  scale_x_continuous(breaks = NULL) +
  theme_bw() +
  theme(
    text = element_text(family='CMUSerif-Roman'),
    axis.line = element_line(colour = 'black'),
    axis.ticks = element_blank(),
    axis.title.x = element_text(family='CMUSerif-Italic'),
    axis.title.y = element_text(family='CMUSerif-Italic'),
    axis.text.x = element_blank()
  )

print(gg)

