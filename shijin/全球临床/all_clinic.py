import datetime
from collections import defaultdict
import json,re

# aa = [(345727, 'NCT01101672', 'submitted', 'December 17, 2013', datetime.date(2013, 12, 17)), (345728, 'NCT01101672', 'returned', 'February 3, 2014', datetime.date(2014, 2, 3)), (345729, 'NCT01099059', 'submitted', 'February 27, 2011', datetime.date(2011, 2, 27)), (345730, 'NCT01099059', 'returned', 'March 24, 2011', datetime.date(2011, 3, 24)), (345731, 'NCT01099059', 'submitted', 'December 6, 2012', datetime.date(2012, 12, 6)), (345732, 'NCT01099059', 'returned', 'January 9, 2013', datetime.date(2013, 1, 9)), (345733, 'NCT01099046', 'submitted', 'July 16, 2015', datetime.date(2015, 7, 16)), (345734, 'NCT01099046', 'returned', 'August 10, 2015', datetime.date(2015, 8, 10)), (345735, 'NCT01098903', 'submitted', 'March 6, 2020', datetime.date(2020, 3, 6)), (345736, 'NCT01098903', 'returned', 'March 19, 2020', datetime.date(2020, 3, 19)), (345737, 'NCT01098903', 'submitted', 'January 15, 2021', datetime.date(2021, 1, 15)), (345738, 'NCT01098604', 'submitted', 'March 19, 2018', datetime.date(2018, 3, 19)), (345739, 'NCT01098604', 'returned', 'October 23, 2018', datetime.date(2018, 10, 23)), (345740, 'NCT01098422', 'submitted', 'May 6, 2020', datetime.date(2020, 5, 6)), (345741, 'NCT01098422', 'returned', 'May 21, 2020', datetime.date(2020, 5, 21)), (345742, 'NCT01097811', 'submitted', 'October 9, 2018', datetime.date(2018, 10, 9)), (345743, 'NCT01097811', 'returned', 'February 20, 2019', datetime.date(2019, 2, 20)), (345744, 'NCT01095952', 'submitted', 'June 27, 2016', datetime.date(2016, 6, 27)), (345745, 'NCT01095952', 'returned', 'August 8, 2016', datetime.date(2016, 8, 8)), (345746, 'NCT01095952', 'submitted', 'October 21, 2019', datetime.date(2019, 10, 21)), (345747, 'NCT01095952', 'returned', 'November 7, 2019', datetime.date(2019, 11, 7)), (345748, 'NCT01094912', 'submitted', 'October 9, 2018', datetime.date(2018, 10, 9)), (345749, 'NCT01094912', 'returned', 'February 20, 2019', datetime.date(2019, 2, 20)), (345750, 'NCT01094353', 'submitted', 'June 20, 2017', datetime.date(2017, 6, 20)), (345751, 'NCT01094353', 'returned', 'November 9, 2017', datetime.date(2017, 11, 9)), (345752, 'NCT01093807', 'submitted', 'October 30, 2020', datetime.date(2020, 10, 30)), (345753, 'NCT01093807', 'returned', 'November 23, 2020', datetime.date(2020, 11, 23)), (345754, 'NCT01093560', 'submitted', 'August 29, 2012', datetime.date(2012, 8, 29)), (345755, 'NCT01093560', 'returned', 'September 28, 2012', datetime.date(2012, 9, 28)), (345756, 'NCT01093560', 'submitted', 'April 10, 2017', datetime.date(2017, 4, 10)), (345757, 'NCT01093560', 'returned', 'June 23, 2017', datetime.date(2017, 6, 23)), (345758, 'NCT01090804', 'submitted', 'August 14, 2012', datetime.date(2012, 8, 14)), (345759, 'NCT01090804', 'returned', 'September 12, 2012', datetime.date(2012, 9, 12)), (345760, 'NCT01089829', 'submitted', 'November 29, 2017', datetime.date(2017, 11, 29)), (345761, 'NCT01089829', 'returned', 'August 23, 2018', datetime.date(2018, 8, 23)), (345762, 'NCT01088971', 'submitted', 'May 12, 2012', datetime.date(2012, 5, 12)), (345763, 'NCT01088971', 'returned', 'June 13, 2012', datetime.date(2012, 6, 13)), (345764, 'NCT01088568', 'submitted', 'April 7, 2011', datetime.date(2011, 4, 7)), (345765, 'NCT01088568', 'returned', 'May 3, 2011', datetime.date(2011, 5, 3)), (345766, 'NCT01088555', 'submitted', 'March 17, 2016', datetime.date(2016, 3, 17)), (345767, 'NCT01088555', 'returned', 'April 18, 2016', datetime.date(2016, 4, 18)), (345768, 'NCT01088139', 'submitted', 'November 18, 2011', datetime.date(2011, 11, 18)), (345769, 'NCT01088139', 'submission_canceled', 'Unknown', None), (345770, 'NCT01088139', 'submitted', 'April 20, 2012', datetime.date(2012, 4, 20)), (345771, 'NCT01088139', 'returned', 'May 17, 2012', datetime.date(2012, 5, 17)), (345772, 'NCT01088139', 'submitted', 'September 28, 2012', datetime.date(2012, 9, 28)), (345773, 'NCT01088139', 'returned', 'October 29, 2012', datetime.date(2012, 10, 29)), (345774, 'NCT01088139', 'submitted', 'October 31, 2012', datetime.date(2012, 10, 31)), (345775, 'NCT01088139', 'returned', 'November 28, 2012', datetime.date(2012, 11, 28)), (345776, 'NCT01088139', 'submitted', 'September 9, 2014', datetime.date(2014, 9, 9)), (345777, 'NCT01088139', 'submission_canceled', 'Unknown', None), (345778, 'NCT01088048', 'submitted', 'January 11, 2021', datetime.date(2021, 1, 11)), (345779, 'NCT01087567', 'submitted', 'September 30, 2020', datetime.date(2020, 9, 30)), (345780, 'NCT01087567', 'returned', 'October 22, 2020', datetime.date(2020, 10, 22)), (345781, 'NCT01087255', 'submitted', 'August 9, 2017', datetime.date(2017, 8, 9)), (345782, 'NCT01087255', 'returned', 'September 7, 2017', datetime.date(2017, 9, 7)), (345784, 'NCT01087164', 'submitted', 'April 11, 2014', datetime.date(2014, 4, 11)), (345785, 'NCT01087164', 'returned', 'May 9, 2014', datetime.date(2014, 5, 9)), (345786, 'NCT01087112', 'submitted', 'December 14, 2020', datetime.date(2020, 12, 14)), (345787, 'NCT01087112', 'returned', 'January 7, 2021', datetime.date(2021, 1, 7)), (345788, 'NCT01086826', 'submitted', 'June 29, 2018', datetime.date(2018, 6, 29)), (345789, 'NCT01086826', 'returned', 'January 9, 2019', datetime.date(2019, 1, 9)), (345790, 'NCT01086826', 'submitted', 'January 10, 2019', datetime.date(2019, 1, 10)), (345791, 'NCT01086826', 'returned', 'April 12, 2019', datetime.date(2019, 4, 12)), (345792, 'NCT01086826', 'submitted', 'May 24, 2019', datetime.date(2019, 5, 24)), (345793, 'NCT01086826', 'returned', 'July 25, 2019', datetime.date(2019, 7, 25)), (345794, 'NCT01085916', 'submitted', 'July 25, 2011', datetime.date(2011, 7, 25)), (345795, 'NCT01085916', 'returned', 'August 19, 2011', datetime.date(2011, 8, 19)), (345796, 'NCT01085747', 'submitted', 'August 20, 2015', datetime.date(2015, 8, 20)), (345797, 'NCT01085747', 'returned', 'September 22, 2015', datetime.date(2015, 9, 22)), (345798, 'NCT01084304', 'submitted', 'April 7, 2017', datetime.date(2017, 4, 7)), (345799, 'NCT01084304', 'submission_canceled', 'Unknown', None), (345800, 'NCT01084304', 'submitted', 'April 18, 2017', datetime.date(2017, 4, 18)), (345801, 'NCT01084304', 'returned', 'July 3, 2017', datetime.date(2017, 7, 3)), (345802, 'NCT01084304', 'submitted', 'February 14, 2018', datetime.date(2018, 2, 14)), (345803, 'NCT01084304', 'returned', 'October 29, 2018', datetime.date(2018, 10, 29)), (345804, 'NCT01084096', 'submitted', 'March 24, 2017', datetime.date(2017, 3, 24)), (345805, 'NCT01084096', 'returned', 'May 5, 2017', datetime.date(2017, 5, 5)), (345806, 'NCT01083433', 'submitted', 'December 3, 2015', datetime.date(2015, 12, 3)), (345807, 'NCT01083433', 'returned', 'January 7, 2016', datetime.date(2016, 1, 7)), (345808, 'NCT01083433', 'submitted', 'November 9, 2018', datetime.date(2018, 11, 9)), (345809, 'NCT01083433', 'returned', 'December 6, 2018', datetime.date(2018, 12, 6)), (345810, 'NCT01081223', 'submitted', 'June 13, 2013', datetime.date(2013, 6, 13)), (345811, 'NCT01081223', 'submission_canceled', 'Unknown', None), (345812, 'NCT01081223', 'submitted', 'December 2, 2013', datetime.date(2013, 12, 2)), (345813, 'NCT01081223', 'submission_canceled', 'Unknown', None), (345814, 'NCT01081223', 'submitted', 'October 21, 2016', datetime.date(2016, 10, 21)), (345815, 'NCT01081223', 'returned', 'December 15, 2016', datetime.date(2016, 12, 15)), (345816, 'NCT01079702', 'submitted', 'August 26, 2014', datetime.date(2014, 8, 26)), (345817, 'NCT01079702', 'returned', 'September 4, 2014', datetime.date(2014, 9, 4)), (345818, 'NCT01079702', 'submitted', 'January 7, 2020', datetime.date(2020, 1, 7)), (345819, 'NCT01079702', 'returned', 'January 21, 2020', datetime.date(2020, 1, 21)), (345820, 'NCT01076725', 'submitted', 'September 19, 2016', datetime.date(2016, 9, 19)), (345821, 'NCT01076725', 'returned', 'November 4, 2016', datetime.date(2016, 11, 4)), (345822, 'NCT01076231', 'submitted', 'April 29, 2020', datetime.date(2020, 4, 29)), (345823, 'NCT01076231', 'returned', 'May 8, 2020', datetime.date(2020, 5, 8)), (345824, 'NCT01076231', 'submitted', 'September 23, 2020', datetime.date(2020, 9, 23)), (345825, 'NCT01076231', 'returned', 'September 24, 2020', datetime.date(2020, 9, 24)), (345826, 'NCT01075945', 'submitted', 'June 10, 2010', datetime.date(2010, 6, 10)), (345827, 'NCT01075945', 'returned', 'July 12, 2010', datetime.date(2010, 7, 12)), (345828, 'NCT01075945', 'submitted', 'August 27, 2010', datetime.date(2010, 8, 27)), (345829, 'NCT01075945', 'returned', 'September 21, 2010', datetime.date(2010, 9, 21)), (345830, 'NCT01075945', 'submitted', 'October 26, 2010', datetime.date(2010, 10, 26)), (345831, 'NCT01075945', 'returned', 'November 24, 2010', datetime.date(2010, 11, 24)), (345832, 'NCT01075945', 'submitted', 'August 5, 2011', datetime.date(2011, 8, 5)), (345833, 'NCT01075945', 'returned', 'September 6, 2011', datetime.date(2011, 9, 6)), (345834, 'NCT01075945', 'submitted', 'June 15, 2012', datetime.date(2012, 6, 15)), (345835, 'NCT01075945', 'returned', 'July 18, 2012', datetime.date(2012, 7, 18)), (345836, 'NCT01075945', 'submitted', 'January 16, 2013', datetime.date(2013, 1, 16)), (345837, 'NCT01075945', 'returned', 'February 19, 2013', datetime.date(2013, 2, 19)), (345838, 'NCT01075945', 'submitted', 'March 2, 2013', datetime.date(2013, 3, 2)), (345839, 'NCT01075945', 'returned', 'April 10, 2013', datetime.date(2013, 4, 10)), (345845, 'NCT01074970', 'submitted', 'October 16, 2020', datetime.date(2020, 10, 16)), (345846, 'NCT01074970', 'returned', 'November 6, 2020', datetime.date(2020, 11, 6)), (345847, 'NCT01074957', 'submitted', 'August 8, 2011', datetime.date(2011, 8, 8)), (345848, 'NCT01074957', 'returned', 'September 9, 2011', datetime.date(2011, 9, 9)), (345849, 'NCT01074957', 'submitted', 'November 25, 2011', datetime.date(2011, 11, 25)), (345850, 'NCT01074957', 'returned', 'December 27, 2011', datetime.date(2011, 12, 27)), (345851, 'NCT01074814', 'submitted', 'May 1, 2017', datetime.date(2017, 5, 1)), (345852, 'NCT01074814', 'returned', 'June 2, 2017', datetime.date(2017, 6, 2)), (345853, 'NCT01074190', 'submitted', 'June 6, 2017', datetime.date(2017, 6, 6)), (345854, 'NCT01074190', 'returned', 'July 5, 2017', datetime.date(2017, 7, 5)), (345855, 'NCT01074190', 'submitted', 'September 13, 2017', datetime.date(2017, 9, 13)), (345856, 'NCT01074190', 'returned', 'October 13, 2017', datetime.date(2017, 10, 13)), (345857, 'NCT01074190', 'submitted', 'June 18, 2020', datetime.date(2020, 6, 18)), (345858, 'NCT01074190', 'returned', 'July 1, 2020', datetime.date(2020, 7, 1)), (345859, 'NCT01073059', 'submitted', 'December 27, 2010', datetime.date(2010, 12, 27)), (345860, 'NCT01073059', 'returned', 'January 11, 2011', datetime.date(2011, 1, 11)), (345861, 'NCT01073059', 'submitted', 'February 14, 2011', datetime.date(2011, 2, 14)), (345862, 'NCT01073059', 'returned', 'March 8, 2011', datetime.date(2011, 3, 8)), (345863, 'NCT01073020', 'submitted', 'January 26, 2021', datetime.date(2021, 1, 26)), (345864, 'NCT01073020', 'submission_canceled', 'January 26, 2021', datetime.date(2021, 1, 26)), (345865, 'NCT01073020', 'submitted', 'January 27, 2021', datetime.date(2021, 1, 27)), (345866, 'NCT01072734', 'submitted', 'August 2, 2013', datetime.date(2013, 8, 2)), (345867, 'NCT01072734', 'returned', 'October 11, 2013', datetime.date(2013, 10, 11)), (345868, 'NCT01072734', 'submitted', 'April 14, 2016', datetime.date(2016, 4, 14)), (345869, 'NCT01072734', 'returned', 'May 20, 2016', datetime.date(2016, 5, 20)), (345870, 'NCT01071525', 'submitted', 'May 6, 2015', datetime.date(2015, 5, 6)), (345871, 'NCT01071525', 'returned', 'May 21, 2015', datetime.date(2015, 5, 21)), (345872, 'NCT01070680', 'submitted', 'December 18, 2020', datetime.date(2020, 12, 18)), (345873, 'NCT01070680', 'returned', 'January 13, 2021', datetime.date(2021, 1, 13)), (345874, 'NCT01070511', 'submitted', 'January 31, 2014', datetime.date(2014, 1, 31)), (345875, 'NCT01070511', 'returned', 'March 13, 2014', datetime.date(2014, 3, 13)), (345876, 'NCT01070511', 'submitted', 'October 31, 2014', datetime.date(2014, 10, 31)), (345877, 'NCT01070511', 'returned', 'November 5, 2014', datetime.date(2014, 11, 5)), (345878, 'NCT01070511', 'submitted', 'November 11, 2014', datetime.date(2014, 11, 11)), (345879, 'NCT01070511', 'returned', 'November 18, 2014', datetime.date(2014, 11, 18)), (345880, 'NCT01070511', 'submitted', 'March 2, 2017', datetime.date(2017, 3, 2)), (345881, 'NCT01070511', 'returned', 'March 30, 2017', datetime.date(2017, 3, 30)), (345882, 'NCT01070511', 'submitted', 'October 15, 2017', datetime.date(2017, 10, 15)), (345883, 'NCT01070511', 'returned', 'November 15, 2017', datetime.date(2017, 11, 15)), (345884, 'NCT01070368', 'submitted', 'March 11, 2013', datetime.date(2013, 3, 11)), (345885, 'NCT01070368', 'returned', 'April 18, 2013', datetime.date(2013, 4, 18)), (345886, 'NCT01070199', 'submitted', 'May 29, 2013', datetime.date(2013, 5, 29)), (345887, 'NCT01070199', 'returned', 'July 25, 2013', datetime.date(2013, 7, 25)), (345888, 'NCT01070199', 'submitted', 'July 30, 2013', datetime.date(2013, 7, 30)), (345889, 'NCT01070199', 'returned', 'August 30, 2013', datetime.date(2013, 8, 30)), (345890, 'NCT01070199', 'submitted', 'November 21, 2013', datetime.date(2013, 11, 21)), (345891, 'NCT01070199', 'returned', 'January 10, 2014', datetime.date(2014, 1, 10)), (345892, 'NCT01070199', 'submitted', 'December 22, 2014', datetime.date(2014, 12, 22)), (345893, 'NCT01070199', 'returned', 'January 3, 2015', datetime.date(2015, 1, 3)), (345894, 'NCT01070199', 'submitted', 'October 14, 2015', datetime.date(2015, 10, 14)), (345895, 'NCT01070199', 'returned', 'November 12, 2015', datetime.date(2015, 11, 12)), (345896, 'NCT01070199', 'submitted', 'March 30, 2016', datetime.date(2016, 3, 30)), (345897, 'NCT01070199', 'returned', 'April 29, 2016', datetime.date(2016, 4, 29)), (345898, 'NCT01070199', 'submitted', 'October 5, 2016', datetime.date(2016, 10, 5)), (345899, 'NCT01070199', 'returned', 'November 28, 2016', datetime.date(2016, 11, 28)), (345900, 'NCT01070199', 'submitted', 'January 16, 2017', datetime.date(2017, 1, 16)), (345901, 'NCT01070199', 'returned', 'March 3, 2017', datetime.date(2017, 3, 3)), (345902, 'NCT01070199', 'submitted', 'April 3, 2017', datetime.date(2017, 4, 3)), (345903, 'NCT01070199', 'returned', 'June 15, 2017', datetime.date(2017, 6, 15)), (345904, 'NCT01070199', 'submitted', 'September 19, 2017', datetime.date(2017, 9, 19)), (345905, 'NCT01070199', 'returned', 'October 19, 2017', datetime.date(2017, 10, 19)), (345906, 'NCT01070069', 'submitted', 'June 23, 2014', datetime.date(2014, 6, 23)), (345907, 'NCT01070069', 'returned', 'July 24, 2014', datetime.date(2014, 7, 24)), (345908, 'NCT01069770', 'submitted', 'September 19, 2016', datetime.date(2016, 9, 19)), (345909, 'NCT01069770', 'returned', 'November 4, 2016', datetime.date(2016, 11, 4)), (345910, 'NCT01069770', 'submitted', 'April 12, 2017', datetime.date(2017, 4, 12)), (345911, 'NCT01069770', 'submission_canceled', 'Unknown', None), (345912, 'NCT01069770', 'submitted', 'April 13, 2017', datetime.date(2017, 4, 13)), (345913, 'NCT01069770', 'returned', 'July 7, 2017', datetime.date(2017, 7, 7)), (345914, 'NCT01068561', 'submitted', 'November 18, 2013', datetime.date(2013, 11, 18)), (345915, 'NCT01068561', 'returned', 'January 9, 2014', datetime.date(2014, 1, 9)), (345916, 'NCT01068561', 'submitted', 'January 12, 2014', datetime.date(2014, 1, 12)), (345917, 'NCT01068561', 'returned', 'March 3, 2014', datetime.date(2014, 3, 3)), (345918, 'NCT01068561', 'submitted', 'July 18, 2017', datetime.date(2017, 7, 18)), (345919, 'NCT01068561', 'returned', 'February 1, 2018', datetime.date(2018, 2, 1)), (345920, 'NCT01068561', 'submitted', 'October 15, 2018', datetime.date(2018, 10, 15)), (345921, 'NCT01068561', 'returned', 'February 19, 2019', datetime.date(2019, 2, 19)), (345922, 'NCT01067170', 'submitted', 'August 16, 2016', datetime.date(2016, 8, 16)), (345923, 'NCT01067170', 'returned', 'October 6, 2016', datetime.date(2016, 10, 6)), (345924, 'NCT01063530', 'submitted', 'May 21, 2013', datetime.date(2013, 5, 21)), (345925, 'NCT01063530', 'returned', 'August 15, 2013', datetime.date(2013, 8, 15)), (345926, 'NCT01063530', 'submitted', 'December 10, 2015', datetime.date(2015, 12, 10)), (345927, 'NCT01063530', 'returned', 'January 14, 2016', datetime.date(2016, 1, 14)), (345928, 'NCT01060943', 'submitted', 'May 7, 2010', datetime.date(2010, 5, 7)), (345929, 'NCT01060943', 'returned', 'June 3, 2010', datetime.date(2010, 6, 3)), (345930, 'NCT01059500', 'submitted', 'July 25, 2016', datetime.date(2016, 7, 25)), (345931, 'NCT01059500', 'returned', 'September 9, 2016', datetime.date(2016, 9, 9)), (345932, 'NCT01059461', 'submitted', 'February 9, 2019', datetime.date(2019, 2, 9)), (345933, 'NCT01059461', 'returned', 'May 9, 2019', datetime.date(2019, 5, 9)), (345934, 'NCT01058512', 'submitted', 'August 4, 2015', datetime.date(2015, 8, 4)), (345935, 'NCT01058512', 'returned', 'August 28, 2015', datetime.date(2015, 8, 28)), (345936, 'NCT01058512', 'submitted', 'October 4, 2016', datetime.date(2016, 10, 4)), (345937, 'NCT01058512', 'returned', 'November 23, 2016', datetime.date(2016, 11, 23)), (345938, 'NCT01058330', 'submitted', 'November 29, 2017', datetime.date(2017, 11, 29)), (345939, 'NCT01058330', 'returned', 'August 22, 2018', datetime.date(2018, 8, 22)), (345940, 'NCT01058330', 'submitted', 'September 13, 2018', datetime.date(2018, 9, 13)), (345941, 'NCT01058330', 'returned', 'February 8, 2019', datetime.date(2019, 2, 8)), (345942, 'NCT01058330', 'submitted', 'October 22, 2020', datetime.date(2020, 10, 22)), (345943, 'NCT01058330', 'returned', 'November 13, 2020', datetime.date(2020, 11, 13)), (345944, 'NCT01058330', 'submitted', 'November 13, 2020', datetime.date(2020, 11, 13)), (345945, 'NCT01058330', 'returned', 'December 10, 2020', datetime.date(2020, 12, 10)), (345946, 'NCT01057602', 'submitted', 'February 12, 2012', datetime.date(2012, 2, 12)), (345947, 'NCT01057602', 'returned', 'March 22, 2012', datetime.date(2012, 3, 22)), (345948, 'NCT01057602', 'submitted', 'March 31, 2012', datetime.date(2012, 3, 31)), (345949, 'NCT01057602', 'returned', 'April 18, 2012', datetime.date(2012, 4, 18)), (345950, 'NCT01057602', 'submitted', 'July 31, 2016', datetime.date(2016, 7, 31)), (345951, 'NCT01057602', 'returned', 'September 20, 2016', datetime.date(2016, 9, 20)), (345953, 'NCT01056458', 'submitted', 'April 4, 2011', datetime.date(2011, 4, 4)), (345954, 'NCT01056458', 'returned', 'April 28, 2011', datetime.date(2011, 4, 28)), (345955, 'NCT01056458', 'submitted', 'May 13, 2011', datetime.date(2011, 5, 13)), (345956, 'NCT01056458', 'returned', 'June 13, 2011', datetime.date(2011, 6, 13)), (345957, 'NCT01056367', 'submitted', 'December 2, 2013', datetime.date(2013, 12, 2)), (345958, 'NCT01056367', 'returned', 'January 16, 2014', datetime.date(2014, 1, 16)), (345959, 'NCT01055392', 'submitted', 'May 10, 2016', datetime.date(2016, 5, 10)), (345960, 'NCT01055392', 'returned', 'June 17, 2016', datetime.date(2016, 6, 17)), (345961, 'NCT01055249', 'submitted', 'June 28, 2011', datetime.date(2011, 6, 28)), (345962, 'NCT01055249', 'returned', 'July 27, 2011', datetime.date(2011, 7, 27)), (345963, 'NCT01055249', 'submitted', 'August 1, 2011', datetime.date(2011, 8, 1)), (345964, 'NCT01055249', 'returned', 'August 29, 2011', datetime.date(2011, 8, 29)), (345965, 'NCT01054664', 'submitted', 'June 27, 2013', datetime.date(2013, 6, 27)), (345966, 'NCT01054664', 'returned', 'September 5, 2013', datetime.date(2013, 9, 5)), (345972, 'NCT01054001', 'submitted', 'May 27, 2015', datetime.date(2015, 5, 27)), (345973, 'NCT01054001', 'returned', 'June 10, 2015', datetime.date(2015, 6, 10)), (345974, 'NCT01053637', 'submitted', 'May 27, 2016', datetime.date(2016, 5, 27)), (345975, 'NCT01053637', 'returned', 'July 7, 2016', datetime.date(2016, 7, 7)), (345976, 'NCT01053637', 'submitted', 'April 25, 2017', datetime.date(2017, 4, 25)), (345977, 'NCT01053637', 'returned', 'June 5, 2017', datetime.date(2017, 6, 5)), (345978, 'NCT01053637', 'submitted', 'April 8, 2019', datetime.date(2019, 4, 8)), (345979, 'NCT01053637', 'returned', 'May 2, 2019', datetime.date(2019, 5, 2)), (345980, 'NCT01053637', 'submitted', 'July 11, 2020', datetime.date(2020, 7, 11)), (345981, 'NCT01053637', 'returned', 'July 28, 2020', datetime.date(2020, 7, 28)), (345982, 'NCT01053637', 'submitted', 'November 6, 2020', datetime.date(2020, 11, 6)), (345983, 'NCT01053637', 'returned', 'November 30, 2020', datetime.date(2020, 11, 30)), (345984, 'NCT01053559', 'submitted', 'April 20, 2016', datetime.date(2016, 4, 20)), (345985, 'NCT01053559', 'returned', 'May 26, 2016', datetime.date(2016, 5, 26)), (345986, 'NCT01053013', 'submitted', 'January 8, 2021', datetime.date(2021, 1, 8)), (345987, 'NCT01052597', 'submitted', 'July 29, 2010', datetime.date(2010, 7, 29)), (345988, 'NCT01052597', 'returned', 'August 24, 2010', datetime.date(2010, 8, 24)), (345994, 'NCT01052155', 'submitted', 'April 5, 2012', datetime.date(2012, 4, 5)), (345995, 'NCT01052155', 'submission_canceled', 'Unknown', None), (345996, 'NCT01052155', 'submitted', 'December 6, 2012', datetime.date(2012, 12, 6)), (345997, 'NCT01052155', 'returned', 'January 16, 2013', datetime.date(2013, 1, 16)), (345998, 'NCT01052155', 'submitted', 'June 18, 2013', datetime.date(2013, 6, 18)), (345999, 'NCT01052155', 'returned', 'August 29, 2013', datetime.date(2013, 8, 29)), (346000, 'NCT01052155', 'submitted', 'April 24, 2017', datetime.date(2017, 4, 24)), (346001, 'NCT01052155', 'returned', 'August 3, 2017', datetime.date(2017, 8, 3)), (346002, 'NCT01051037', 'submitted', 'September 1, 2020', datetime.date(2020, 9, 1)), (346003, 'NCT01051037', 'returned', 'September 25, 2020', datetime.date(2020, 9, 25)), (346004, 'NCT01050881', 'submitted', 'September 19, 2017', datetime.date(2017, 9, 19)), (346005, 'NCT01050881', 'returned', 'July 11, 2018', datetime.date(2018, 7, 11)), (346006, 'NCT01050231', 'submitted', 'October 25, 2016', datetime.date(2016, 10, 25)), (346007, 'NCT01050231', 'submission_canceled', 'Unknown', None), (346008, 'NCT01050231', 'submitted', 'October 28, 2016', datetime.date(2016, 10, 28)), (346009, 'NCT01050231', 'returned', 'December 22, 2016', datetime.date(2016, 12, 22)), (346010, 'NCT01050114', 'submitted', 'March 23, 2020', datetime.date(2020, 3, 23)), (346011, 'NCT01050114', 'returned', 'April 3, 2020', datetime.date(2020, 4, 3)), (346012, 'NCT01050114', 'submitted', 'June 8, 2020', datetime.date(2020, 6, 8)), (346013, 'NCT01050114', 'returned', 'June 19, 2020', datetime.date(2020, 6, 19)), (346014, 'NCT01050114', 'submitted', 'July 22, 2020', datetime.date(2020, 7, 22)), (346015, 'NCT01050114', 'returned', 'August 5, 2020', datetime.date(2020, 8, 5)), (346016, 'NCT01050114', 'submitted', 'January 4, 2021', datetime.date(2021, 1, 4)), (346017, 'NCT01050114', 'returned', 'January 22, 2021', datetime.date(2021, 1, 22)), (346018, 'NCT01049919', 'submitted', 'January 22, 2021', datetime.date(2021, 1, 22)), (346019, 'NCT01049828', 'submitted', 'December 17, 2013', datetime.date(2013, 12, 17)), (346020, 'NCT01049828', 'returned', 'February 10, 2014', datetime.date(2014, 2, 10)), (346021, 'NCT01049828', 'submitted', 'February 10, 2014', datetime.date(2014, 2, 10)), (346022, 'NCT01049828', 'returned', 'March 27, 2014', datetime.date(2014, 3, 27)), (346023, 'NCT01049399', 'submitted', 'October 24, 2012', datetime.date(2012, 10, 24)), (346024, 'NCT01049399', 'returned', 'November 23, 2012', datetime.date(2012, 11, 23)), (346025, 'NCT01049399', 'submitted', 'November 23, 2012', datetime.date(2012, 11, 23)), (346026, 'NCT01049399', 'returned', 'December 21, 2012', datetime.date(2012, 12, 21)), (346027, 'NCT01048554', 'submitted', 'May 8, 2014', datetime.date(2014, 5, 8)), (346028, 'NCT01048554', 'returned', 'June 9, 2014', datetime.date(2014, 6, 9)), (346029, 'NCT01048307', 'submitted', 'August 23, 2011', datetime.date(2011, 8, 23)), (346030, 'NCT01048307', 'returned', 'September 27, 2011', datetime.date(2011, 9, 27)), (346031, 'NCT01048307', 'submitted', 'February 12, 2013', datetime.date(2013, 2, 12)), (346032, 'NCT01048307', 'returned', 'March 13, 2013', datetime.date(2013, 3, 13)), (346033, 'NCT01048307', 'submitted', 'July 22, 2014', datetime.date(2014, 7, 22)), (346034, 'NCT01048307', 'returned', 'August 12, 2014', datetime.date(2014, 8, 12)), (346035, 'NCT01047397', 'submitted', 'December 4, 2017', datetime.date(2017, 12, 4)), (346036, 'NCT01047397', 'submission_canceled', 'Unknown', None), (346037, 'NCT01047397', 'submitted', 'December 13, 2017', datetime.date(2017, 12, 13)), (346038, 'NCT01047397', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346039, 'NCT01046812', 'submitted', 'September 22, 2019', datetime.date(2019, 9, 22)), (346040, 'NCT01046812', 'returned', 'October 11, 2019', datetime.date(2019, 10, 11)), (346041, 'NCT01046461', 'submitted', 'October 11, 2012', datetime.date(2012, 10, 11)), (346042, 'NCT01046461', 'returned', 'November 8, 2012', datetime.date(2012, 11, 8)), (346043, 'NCT01045954', 'submitted', 'June 17, 2011', datetime.date(2011, 6, 17)), (346044, 'NCT01045954', 'returned', 'July 14, 2011', datetime.date(2011, 7, 14)), (346045, 'NCT01045954', 'submitted', 'August 23, 2013', datetime.date(2013, 8, 23)), (346046, 'NCT01045954', 'returned', 'October 27, 2013', datetime.date(2013, 10, 27)), (346047, 'NCT01045590', 'submitted', 'July 12, 2017', datetime.date(2017, 7, 12)), (346048, 'NCT01045590', 'returned', 'February 2, 2018', datetime.date(2018, 2, 2)), (346049, 'NCT01045590', 'submitted', 'February 15, 2018', datetime.date(2018, 2, 15)), (346050, 'NCT01045590', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346053, 'NCT01043328', 'submitted', 'June 4, 2015', datetime.date(2015, 6, 4)), (346054, 'NCT01043328', 'returned', 'June 26, 2015', datetime.date(2015, 6, 26)), (346055, 'NCT01042951', 'submitted', 'August 19, 2017', datetime.date(2017, 8, 19)), (346056, 'NCT01042951', 'returned', 'March 1, 2018', datetime.date(2018, 3, 1)), (346057, 'NCT01042951', 'submitted', 'April 9, 2018', datetime.date(2018, 4, 9)), (346058, 'NCT01042951', 'returned', 'November 8, 2018', datetime.date(2018, 11, 8)), (346059, 'NCT01041508', 'submitted', 'October 2, 2018', datetime.date(2018, 10, 2)), (346060, 'NCT01041508', 'returned', 'February 18, 2019', datetime.date(2019, 2, 18)), (346061, 'NCT01041495', 'submitted', 'December 9, 2014', datetime.date(2014, 12, 9)), (346062, 'NCT01041495', 'returned', 'December 17, 2014', datetime.date(2014, 12, 17)), (346063, 'NCT01041495', 'submitted', 'August 27, 2020', datetime.date(2020, 8, 27)), (346064, 'NCT01041495', 'returned', 'September 15, 2020', datetime.date(2020, 9, 15)), (346065, 'NCT01041313', 'submitted', 'March 31, 2017', datetime.date(2017, 3, 31)), (346066, 'NCT01041313', 'returned', 'May 10, 2017', datetime.date(2017, 5, 10)), (346072, 'NCT01041183', 'submitted', 'July 23, 2010', datetime.date(2010, 7, 23)), (346073, 'NCT01041183', 'returned', 'August 18, 2010', datetime.date(2010, 8, 18)), (346074, 'NCT01041066', 'submitted', 'September 7, 2010', datetime.date(2010, 9, 7)), (346075, 'NCT01041066', 'returned', 'September 27, 2010', datetime.date(2010, 9, 27)), (346076, 'NCT01040910', 'submitted', 'April 14, 2013', datetime.date(2013, 4, 14)), (346077, 'NCT01040910', 'returned', 'May 30, 2013', datetime.date(2013, 5, 30)), (346078, 'NCT01040910', 'submitted', 'June 7, 2020', datetime.date(2020, 6, 7)), (346079, 'NCT01040910', 'submission_canceled', 'June 7, 2020', datetime.date(2020, 6, 7)), (346080, 'NCT01040910', 'submitted', 'June 15, 2020', datetime.date(2020, 6, 15)), (346081, 'NCT01040910', 'returned', 'July 1, 2020', datetime.date(2020, 7, 1)), (346082, 'NCT01040195', 'submitted', 'June 10, 2018', datetime.date(2018, 6, 10)), (346083, 'NCT01040195', 'returned', 'December 21, 2018', datetime.date(2018, 12, 21)), (346084, 'NCT01040000', 'submitted', 'January 17, 2018', datetime.date(2018, 1, 17)), (346085, 'NCT01040000', 'returned', 'February 15, 2018', datetime.date(2018, 2, 15)), (346086, 'NCT01040000', 'submitted', 'March 2, 2018', datetime.date(2018, 3, 2)), (346087, 'NCT01040000', 'returned', 'March 29, 2018', datetime.date(2018, 3, 29)), (346088, 'NCT01039805', 'submitted', 'August 14, 2017', datetime.date(2017, 8, 14)), (346089, 'NCT01039805', 'returned', 'March 2, 2018', datetime.date(2018, 3, 2)), (346090, 'NCT01039805', 'submitted', 'March 8, 2018', datetime.date(2018, 3, 8)), (346091, 'NCT01039805', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346092, 'NCT01039701', 'submitted', 'July 23, 2014', datetime.date(2014, 7, 23)), (346093, 'NCT01039701', 'returned', 'August 12, 2014', datetime.date(2014, 8, 12)), (346094, 'NCT01039298', 'submitted', 'October 15, 2020', datetime.date(2020, 10, 15)), (346095, 'NCT01039298', 'returned', 'November 4, 2020', datetime.date(2020, 11, 4)), (346096, 'NCT01039233', 'submitted', 'February 8, 2010', datetime.date(2010, 2, 8)), (346097, 'NCT01039233', 'returned', 'February 25, 2010', datetime.date(2010, 2, 25)), (346098, 'NCT01039233', 'submitted', 'August 12, 2010', datetime.date(2010, 8, 12)), (346099, 'NCT01039233', 'returned', 'September 1, 2010', datetime.date(2010, 9, 1)), (346100, 'NCT01039233', 'submitted', 'June 23, 2011', datetime.date(2011, 6, 23)), (346101, 'NCT01039233', 'returned', 'July 22, 2011', datetime.date(2011, 7, 22)), (346102, 'NCT01039233', 'submitted', 'July 27, 2011', datetime.date(2011, 7, 27)), (346103, 'NCT01039233', 'returned', 'August 29, 2011', datetime.date(2011, 8, 29)), (346112, 'NCT01038765', 'submitted', 'January 25, 2021', datetime.date(2021, 1, 25)), (346113, 'NCT01038453', 'submitted', 'May 13, 2016', datetime.date(2016, 5, 13)), (346114, 'NCT01038453', 'returned', 'June 20, 2016', datetime.date(2016, 6, 20)), (346116, 'NCT01037816', 'submitted', 'September 4, 2020', datetime.date(2020, 9, 4)), (346117, 'NCT01037816', 'returned', 'September 28, 2020', datetime.date(2020, 9, 28)), (346118, 'NCT01037816', 'submitted', 'September 30, 2020', datetime.date(2020, 9, 30)), (346119, 'NCT01037816', 'returned', 'October 22, 2020', datetime.date(2020, 10, 22)), (346120, 'NCT01037738', 'submitted', 'January 15, 2010', datetime.date(2010, 1, 15)), (346121, 'NCT01037738', 'returned', 'February 3, 2010', datetime.date(2010, 2, 3)), (346122, 'NCT01037738', 'submitted', 'February 5, 2010', datetime.date(2010, 2, 5)), (346123, 'NCT01037738', 'returned', 'February 22, 2010', datetime.date(2010, 2, 22)), (346124, 'NCT01036659', 'submitted', 'October 30, 2014', datetime.date(2014, 10, 30)), (346125, 'NCT01036659', 'returned', 'November 4, 2014', datetime.date(2014, 11, 4)), (346126, 'NCT01035021', 'submitted', 'June 4, 2015', datetime.date(2015, 6, 4)), (346127, 'NCT01035021', 'returned', 'June 29, 2015', datetime.date(2015, 6, 29)), (346128, 'NCT01033708', 'submitted', 'January 27, 2014', datetime.date(2014, 1, 27)), (346129, 'NCT01033708', 'submission_canceled', 'Unknown', None), (346130, 'NCT01033708', 'submitted', 'January 28, 2014', datetime.date(2014, 1, 28)), (346131, 'NCT01033708', 'returned', 'March 11, 2014', datetime.date(2014, 3, 11)), (346132, 'NCT01032304', 'submitted', 'September 13, 2016', datetime.date(2016, 9, 13)), (346133, 'NCT01032304', 'returned', 'November 2, 2016', datetime.date(2016, 11, 2)), (346134, 'NCT01032304', 'submitted', 'November 21, 2016', datetime.date(2016, 11, 21)), (346135, 'NCT01032304', 'submission_canceled', 'Unknown', None), (346136, 'NCT01032304', 'submitted', 'January 10, 2017', datetime.date(2017, 1, 10)), (346137, 'NCT01032304', 'returned', 'February 28, 2017', datetime.date(2017, 2, 28)), (346138, 'NCT01032304', 'submitted', 'May 12, 2017', datetime.date(2017, 5, 12)), (346139, 'NCT01032304', 'submission_canceled', 'Unknown', None), (346140, 'NCT01032304', 'submitted', 'May 17, 2017', datetime.date(2017, 5, 17)), (346141, 'NCT01032304', 'returned', 'December 18, 2017', datetime.date(2017, 12, 18)), (346142, 'NCT01032304', 'submitted', 'February 6, 2018', datetime.date(2018, 2, 6)), (346143, 'NCT01032304', 'returned', 'February 7, 2018', datetime.date(2018, 2, 7)), (346144, 'NCT01032304', 'submitted', 'February 9, 2018', datetime.date(2018, 2, 9)), (346145, 'NCT01032304', 'returned', 'October 26, 2018', datetime.date(2018, 10, 26)), (346146, 'NCT01032083', 'submitted', 'March 13, 2019', datetime.date(2019, 3, 13)), (346147, 'NCT01032083', 'returned', 'June 14, 2019', datetime.date(2019, 6, 14)), (346148, 'NCT01032083', 'submitted', 'August 7, 2019', datetime.date(2019, 8, 7)), (346149, 'NCT01032083', 'returned', 'September 12, 2019', datetime.date(2019, 9, 12)), (346150, 'NCT01031511', 'submitted', 'October 30, 2013', datetime.date(2013, 10, 30)), (346151, 'NCT01031511', 'returned', 'December 19, 2013', datetime.date(2013, 12, 19)), (346152, 'NCT01031511', 'submitted', 'December 23, 2013', datetime.date(2013, 12, 23)), (346153, 'NCT01031511', 'returned', 'February 8, 2014', datetime.date(2014, 2, 8)), (346154, 'NCT01030848', 'submitted', 'October 25, 2013', datetime.date(2013, 10, 25)), (346155, 'NCT01030848', 'returned', 'December 16, 2013', datetime.date(2013, 12, 16)), (346156, 'NCT01030614', 'submitted', 'March 23, 2015', datetime.date(2015, 3, 23)), (346157, 'NCT01030614', 'returned', 'March 31, 2015', datetime.date(2015, 3, 31)), (346158, 'NCT01030614', 'submitted', 'March 31, 2015', datetime.date(2015, 3, 31)), (346159, 'NCT01030614', 'returned', 'April 21, 2015', datetime.date(2015, 4, 21)), (346160, 'NCT01030575', 'submitted', 'December 23, 2020', datetime.date(2020, 12, 23)), (346161, 'NCT01030575', 'returned', 'January 19, 2021', datetime.date(2021, 1, 19)), (346162, 'NCT01029678', 'submitted', 'September 15, 2018', datetime.date(2018, 9, 15)), (346163, 'NCT01029678', 'returned', 'February 12, 2019', datetime.date(2019, 2, 12)), (346164, 'NCT01029496', 'submitted', 'October 7, 2010', datetime.date(2010, 10, 7)), (346165, 'NCT01029496', 'returned', 'November 5, 2010', datetime.date(2010, 11, 5)), (346166, 'NCT01029353', 'submitted', 'September 2, 2020', datetime.date(2020, 9, 2)), (346167, 'NCT01029353', 'returned', 'September 24, 2020', datetime.date(2020, 9, 24)), (346168, 'NCT01029353', 'submitted', 'November 19, 2020', datetime.date(2020, 11, 19)), (346169, 'NCT01029353', 'returned', 'December 17, 2020', datetime.date(2020, 12, 17)), (346170, 'NCT01028287', 'submitted', 'August 19, 2013', datetime.date(2013, 8, 19)), (346171, 'NCT01028287', 'returned', 'October 30, 2013', datetime.date(2013, 10, 30)), (346172, 'NCT01028287', 'submitted', 'January 23, 2017', datetime.date(2017, 1, 23)), (346173, 'NCT01028287', 'returned', 'March 10, 2017', datetime.date(2017, 3, 10)), (346174, 'NCT01028287', 'submitted', 'October 3, 2017', datetime.date(2017, 10, 3)), (346175, 'NCT01028287', 'returned', 'November 2, 2017', datetime.date(2017, 11, 2)), (346176, 'NCT01028287', 'submitted', 'November 8, 2017', datetime.date(2017, 11, 8)), (346177, 'NCT01028287', 'returned', 'December 8, 2017', datetime.date(2017, 12, 8)), (346178, 'NCT01027676', 'submitted', 'March 3, 2015', datetime.date(2015, 3, 3)), (346179, 'NCT01027676', 'returned', 'March 13, 2015', datetime.date(2015, 3, 13)), (346180, 'NCT01027455', 'submitted', 'September 14, 2011', datetime.date(2011, 9, 14)), (346181, 'NCT01027455', 'returned', 'October 19, 2011', datetime.date(2011, 10, 19)), (346182, 'NCT01027455', 'submitted', 'December 9, 2013', datetime.date(2013, 12, 9)), (346183, 'NCT01027455', 'returned', 'January 23, 2014', datetime.date(2014, 1, 23)), (346184, 'NCT01027182', 'submitted', 'January 23, 2018', datetime.date(2018, 1, 23)), (346185, 'NCT01027182', 'returned', 'September 21, 2018', datetime.date(2018, 9, 21)), (346186, 'NCT01026311', 'submitted', 'September 4, 2020', datetime.date(2020, 9, 4)), (346187, 'NCT01026311', 'returned', 'September 25, 2020', datetime.date(2020, 9, 25)), (346188, 'NCT01026272', 'submitted', 'May 15, 2017', datetime.date(2017, 5, 15)), (346189, 'NCT01026272', 'returned', 'October 10, 2017', datetime.date(2017, 10, 10)), (346190, 'NCT01026272', 'submitted', 'December 8, 2017', datetime.date(2017, 12, 8)), (346191, 'NCT01026272', 'returned', 'October 4, 2018', datetime.date(2018, 10, 4)), (346192, 'NCT01025609', 'submitted', 'July 26, 2017', datetime.date(2017, 7, 26)), (346193, 'NCT01025609', 'returned', 'January 29, 2018', datetime.date(2018, 1, 29)), (346194, 'NCT01025609', 'submitted', 'March 1, 2018', datetime.date(2018, 3, 1)), (346195, 'NCT01025609', 'returned', 'November 6, 2018', datetime.date(2018, 11, 6)), (346196, 'NCT01024361', 'submitted', 'January 23, 2012', datetime.date(2012, 1, 23)), (346197, 'NCT01024361', 'returned', 'February 23, 2012', datetime.date(2012, 2, 23)), (346198, 'NCT01024361', 'submitted', 'December 2, 2014', datetime.date(2014, 12, 2)), (346199, 'NCT01024361', 'returned', 'December 2, 2014', datetime.date(2014, 12, 2)), (346200, 'NCT01024231', 'submitted', 'August 28, 2020', datetime.date(2020, 8, 28)), (346201, 'NCT01024231', 'returned', 'September 22, 2020', datetime.date(2020, 9, 22)), (346202, 'NCT01024231', 'submitted', 'October 16, 2020', datetime.date(2020, 10, 16)), (346203, 'NCT01024231', 'returned', 'November 6, 2020', datetime.date(2020, 11, 6)), (346204, 'NCT01024231', 'submitted', 'January 6, 2021', datetime.date(2021, 1, 6)), (346205, 'NCT01024231', 'returned', 'January 27, 2021', datetime.date(2021, 1, 27)), (346206, 'NCT01024023', 'submitted', 'April 7, 2015', datetime.date(2015, 4, 7)), (346207, 'NCT01024023', 'returned', 'April 20, 2015', datetime.date(2015, 4, 20)), (346208, 'NCT01022580', 'submitted', 'August 26, 2015', datetime.date(2015, 8, 26)), (346209, 'NCT01022580', 'returned', 'September 25, 2015', datetime.date(2015, 9, 25)), (346210, 'NCT01022580', 'submitted', 'October 9, 2015', datetime.date(2015, 10, 9)), (346211, 'NCT01022580', 'returned', 'November 6, 2015', datetime.date(2015, 11, 6)), (346212, 'NCT01022580', 'submitted', 'December 3, 2015', datetime.date(2015, 12, 3)), (346213, 'NCT01022580', 'returned', 'January 7, 2016', datetime.date(2016, 1, 7)), (346214, 'NCT01021267', 'submitted', 'November 22, 2011', datetime.date(2011, 11, 22)), (346215, 'NCT01021267', 'returned', 'December 22, 2011', datetime.date(2011, 12, 22)), (346216, 'NCT01021267', 'submitted', 'February 6, 2020', datetime.date(2020, 2, 6)), (346217, 'NCT01021267', 'returned', 'February 17, 2020', datetime.date(2020, 2, 17)), (346218, 'NCT01020630', 'submitted', 'August 9, 2018', datetime.date(2018, 8, 9)), (346219, 'NCT01020630', 'returned', 'January 24, 2019', datetime.date(2019, 1, 24)), (346220, 'NCT01020409', 'submitted', 'July 8, 2018', datetime.date(2018, 7, 8)), (346221, 'NCT01020409', 'returned', 'January 11, 2019', datetime.date(2019, 1, 11)), (346222, 'NCT01019889', 'submitted', 'March 10, 2014', datetime.date(2014, 3, 10)), (346223, 'NCT01019889', 'returned', 'April 15, 2014', datetime.date(2014, 4, 15)), (346224, 'NCT01019889', 'submitted', 'February 22, 2016', datetime.date(2016, 2, 22)), (346225, 'NCT01019889', 'returned', 'March 22, 2016', datetime.date(2016, 3, 22)), (346226, 'NCT01019889', 'submitted', 'August 13, 2019', datetime.date(2019, 8, 13)), (346227, 'NCT01019889', 'returned', 'August 23, 2019', datetime.date(2019, 8, 23)), (346228, 'NCT01019733', 'submitted', 'September 3, 2014', datetime.date(2014, 9, 3)), (346229, 'NCT01019733', 'returned', 'September 9, 2014', datetime.date(2014, 9, 9)), (346230, 'NCT01019083', 'submitted', 'August 27, 2017', datetime.date(2017, 8, 27)), (346231, 'NCT01019083', 'returned', 'March 22, 2018', datetime.date(2018, 3, 22)), (346232, 'NCT01019083', 'submitted', 'October 31, 2018', datetime.date(2018, 10, 31)), (346233, 'NCT01019083', 'returned', 'February 28, 2019', datetime.date(2019, 2, 28)), (346234, 'NCT01018017', 'submitted', 'September 6, 2017', datetime.date(2017, 9, 6)), (346235, 'NCT01018017', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346236, 'NCT01016561', 'submitted', 'April 24, 2020', datetime.date(2020, 4, 24)), (346237, 'NCT01016561', 'returned', 'May 6, 2020', datetime.date(2020, 5, 6)), (346238, 'NCT01016561', 'submitted', 'November 2, 2020', datetime.date(2020, 11, 2)), (346239, 'NCT01016561', 'returned', 'November 23, 2020', datetime.date(2020, 11, 23)), (346240, 'NCT01014338', 'submitted', 'July 31, 2019', datetime.date(2019, 7, 31)), (346241, 'NCT01014338', 'returned', 'September 6, 2019', datetime.date(2019, 9, 6)), (346242, 'NCT01013532', 'submitted', 'December 28, 2016', datetime.date(2016, 12, 28)), (346243, 'NCT01013532', 'returned', 'February 21, 2017', datetime.date(2017, 2, 21)), (346244, 'NCT01013077', 'submitted', 'December 17, 2012', datetime.date(2012, 12, 17)), (346245, 'NCT01013077', 'returned', 'January 22, 2013', datetime.date(2013, 1, 22)), (346246, 'NCT01013077', 'submitted', 'November 19, 2015', datetime.date(2015, 11, 19)), (346247, 'NCT01013077', 'returned', 'December 24, 2015', datetime.date(2015, 12, 24)), (346248, 'NCT01012843', 'submitted', 'November 16, 2009', datetime.date(2009, 11, 16)), (346249, 'NCT01012843', 'returned', 'December 22, 2009', datetime.date(2009, 12, 22)), (346250, 'NCT01012843', 'submitted', 'December 23, 2009', datetime.date(2009, 12, 23)), (346251, 'NCT01012843', 'returned', 'January 26, 2010', datetime.date(2010, 1, 26)), (346252, 'NCT01012830', 'submitted', 'January 23, 2018', datetime.date(2018, 1, 23)), (346253, 'NCT01012830', 'returned', 'February 19, 2018', datetime.date(2018, 2, 19)), (346254, 'NCT01012609', 'submitted', 'October 5, 2020', datetime.date(2020, 10, 5)), (346255, 'NCT01012609', 'returned', 'October 27, 2020', datetime.date(2020, 10, 27)), (346256, 'NCT01012609', 'submitted', 'October 28, 2020', datetime.date(2020, 10, 28)), (346257, 'NCT01012609', 'returned', 'November 19, 2020', datetime.date(2020, 11, 19)), (346258, 'NCT01012609', 'submitted', 'November 20, 2020', datetime.date(2020, 11, 20)), (346259, 'NCT01012609', 'returned', 'December 15, 2020', datetime.date(2020, 12, 15)), (346260, 'NCT01012609', 'submitted', 'December 30, 2020', datetime.date(2020, 12, 30)), (346261, 'NCT01012609', 'returned', 'January 19, 2021', datetime.date(2021, 1, 19)), (346262, 'NCT01012375', 'submitted', 'July 24, 2014', datetime.date(2014, 7, 24)), (346263, 'NCT01012375', 'returned', 'August 13, 2014', datetime.date(2014, 8, 13)), (346264, 'NCT01011374', 'submitted', 'September 19, 2019', datetime.date(2019, 9, 19)), (346265, 'NCT01011374', 'returned', 'October 10, 2019', datetime.date(2019, 10, 10)), (346266, 'NCT01011192', 'submitted', 'November 13, 2009', datetime.date(2009, 11, 13)), (346267, 'NCT01011192', 'returned', 'December 14, 2009', datetime.date(2009, 12, 14)), (346268, 'NCT01010789', 'submitted', 'January 21, 2016', datetime.date(2016, 1, 21)), (346269, 'NCT01010789', 'returned', 'February 17, 2016', datetime.date(2016, 2, 17)), (346270, 'NCT01010789', 'submitted', 'March 25, 2019', datetime.date(2019, 3, 25)), (346271, 'NCT01010789', 'returned', 'April 15, 2019', datetime.date(2019, 4, 15)), (346272, 'NCT01010789', 'submitted', 'October 14, 2020', datetime.date(2020, 10, 14)), (346273, 'NCT01010789', 'returned', 'November 4, 2020', datetime.date(2020, 11, 4)), (346274, 'NCT01010516', 'submitted', 'December 2, 2015', datetime.date(2015, 12, 2)), (346275, 'NCT01010516', 'returned', 'January 6, 2016', datetime.date(2016, 1, 6)), (346276, 'NCT01010516', 'submitted', 'July 20, 2016', datetime.date(2016, 7, 20)), (346277, 'NCT01010516', 'returned', 'August 31, 2016', datetime.date(2016, 8, 31)), (346278, 'NCT01009970', 'submitted', 'January 20, 2017', datetime.date(2017, 1, 20)), (346279, 'NCT01009970', 'returned', 'March 9, 2017', datetime.date(2017, 3, 9)), (346280, 'NCT01009970', 'submitted', 'February 5, 2020', datetime.date(2020, 2, 5)), (346281, 'NCT01009970', 'submission_canceled', 'February 6, 2020', datetime.date(2020, 2, 6)), (346282, 'NCT01009970', 'submitted', 'February 6, 2020', datetime.date(2020, 2, 6)), (346283, 'NCT01009970', 'returned', 'February 17, 2020', datetime.date(2020, 2, 17)), (346284, 'NCT01009918', 'submitted', 'January 12, 2021', datetime.date(2021, 1, 12)), (346285, 'NCT01009671', 'submitted', 'March 27, 2012', datetime.date(2012, 3, 27)), (346286, 'NCT01009671', 'returned', 'April 18, 2012', datetime.date(2012, 4, 18)), (346287, 'NCT01009671', 'submitted', 'May 9, 2012', datetime.date(2012, 5, 9)), (346288, 'NCT01009671', 'returned', 'June 12, 2012', datetime.date(2012, 6, 12)), (346289, 'NCT01009671', 'submitted', 'June 12, 2012', datetime.date(2012, 6, 12)), (346290, 'NCT01009671', 'returned', 'July 13, 2012', datetime.date(2012, 7, 13)), (346291, 'NCT01009255', 'submitted', 'April 13, 2017', datetime.date(2017, 4, 13)), (346292, 'NCT01009255', 'returned', 'June 28, 2017', datetime.date(2017, 6, 28)), (346293, 'NCT01009255', 'submitted', 'July 23, 2017', datetime.date(2017, 7, 23)), (346294, 'NCT01009255', 'returned', 'February 5, 2018', datetime.date(2018, 2, 5)), (346295, 'NCT01006733', 'submitted', 'January 27, 2018', datetime.date(2018, 1, 27)), (346296, 'NCT01006733', 'returned', 'February 26, 2018', datetime.date(2018, 2, 26)), (346297, 'NCT01006733', 'submitted', 'March 16, 2020', datetime.date(2020, 3, 16)), (346298, 'NCT01006733', 'returned', 'April 2, 2020', datetime.date(2020, 4, 2)), (346299, 'NCT01006499', 'submitted', 'August 2, 2013', datetime.date(2013, 8, 2)), (346300, 'NCT01006499', 'submission_canceled', 'Unknown', None), (346301, 'NCT01006499', 'submitted', 'August 25, 2013', datetime.date(2013, 8, 25)), (346302, 'NCT01006499', 'returned', 'October 30, 2013', datetime.date(2013, 10, 30)), (346303, 'NCT01006369', 'submitted', 'March 17, 2017', datetime.date(2017, 3, 17)), (346304, 'NCT01006369', 'returned', 'April 28, 2017', datetime.date(2017, 4, 28)), (346305, 'NCT01004718', 'submitted', 'September 11, 2020', datetime.date(2020, 9, 11)), (346306, 'NCT01004718', 'returned', 'October 2, 2020', datetime.date(2020, 10, 2)), (346307, 'NCT01004055', 'submitted', 'March 8, 2011', datetime.date(2011, 3, 8)), (346308, 'NCT01004055', 'returned', 'April 4, 2011', datetime.date(2011, 4, 4)), (346309, 'NCT01004055', 'submitted', 'May 10, 2011', datetime.date(2011, 5, 10)), (346310, 'NCT01004055', 'returned', 'June 8, 2011', datetime.date(2011, 6, 8)), (346311, 'NCT01004055', 'submitted', 'February 21, 2012', datetime.date(2012, 2, 21)), (346312, 'NCT01004055', 'returned', 'March 26, 2012', datetime.date(2012, 3, 26)), (346313, 'NCT01004055', 'submitted', 'June 18, 2015', datetime.date(2015, 6, 18)), (346314, 'NCT01004055', 'returned', 'July 10, 2015', datetime.date(2015, 7, 10)), (346315, 'NCT01002794', 'submitted', 'April 3, 2018', datetime.date(2018, 4, 3)), (346316, 'NCT01002794', 'returned', 'November 6, 2018', datetime.date(2018, 11, 6)), (346317, 'NCT01002794', 'submitted', 'November 4, 2020', datetime.date(2020, 11, 4)), (346318, 'NCT01002794', 'returned', 'December 1, 2020', datetime.date(2020, 12, 1)), (346319, 'NCT01001910', 'submitted', 'August 31, 2020', datetime.date(2020, 8, 31)), (346320, 'NCT01001910', 'returned', 'September 18, 2020', datetime.date(2020, 9, 18)), (346321, 'NCT01001910', 'submitted', 'December 16, 2020', datetime.date(2020, 12, 16)), (346322, 'NCT01001910', 'returned', 'January 8, 2021', datetime.date(2021, 1, 8)), (346323, 'NCT01001897', 'submitted', 'June 17, 2013', datetime.date(2013, 6, 17)), (346324, 'NCT01001897', 'returned', 'August 21, 2013', datetime.date(2013, 8, 21)), (346325, 'NCT01001338', 'submitted', 'August 12, 2017', datetime.date(2017, 8, 12)), (346326, 'NCT01001338', 'submission_canceled', 'Unknown', None), (346327, 'NCT01001338', 'submitted', 'August 17, 2017', datetime.date(2017, 8, 17)), (346328, 'NCT01001338', 'returned', 'September 19, 2017', datetime.date(2017, 9, 19)), (346329, 'NCT01001338', 'submitted', 'November 28, 2017', datetime.date(2017, 11, 28)), (346330, 'NCT01001338', 'returned', 'December 21, 2017', datetime.date(2017, 12, 21)), (346331, 'NCT01000714', 'submitted', 'August 23, 2010', datetime.date(2010, 8, 23)), (346332, 'NCT01000714', 'returned', 'August 24, 2010', datetime.date(2010, 8, 24)), (346333, 'NCT01000636', 'submitted', 'June 25, 2013', datetime.date(2013, 6, 25)), (346334, 'NCT01000636', 'returned', 'September 3, 2013', datetime.date(2013, 9, 3)), (346335, 'NCT01000636', 'submitted', 'March 24, 2014', datetime.date(2014, 3, 24)), (346336, 'NCT01000636', 'returned', 'April 25, 2014', datetime.date(2014, 4, 25)), (346337, 'NCT01000272', 'submitted', 'June 8, 2015', datetime.date(2015, 6, 8)), (346338, 'NCT01000272', 'returned', 'June 29, 2015', datetime.date(2015, 6, 29)), (346339, 'NCT01000272', 'submitted', 'August 2, 2015', datetime.date(2015, 8, 2)), (346340, 'NCT01000272', 'submission_canceled', 'Unknown', None), (346341, 'NCT01000272', 'submitted', 'August 11, 2015', datetime.date(2015, 8, 11)), (346342, 'NCT01000272', 'returned', 'September 14, 2015', datetime.date(2015, 9, 14)), (346343, 'NCT00999505', 'submitted', 'August 17, 2016', datetime.date(2016, 8, 17)), (346344, 'NCT00999505', 'returned', 'October 10, 2016', datetime.date(2016, 10, 10)), (346345, 'NCT00999505', 'submitted', 'February 22, 2017', datetime.date(2017, 2, 22)), (346346, 'NCT00999505', 'returned', 'April 5, 2017', datetime.date(2017, 4, 5)), (346347, 'NCT00999492', 'submitted', 'August 4, 2014', datetime.date(2014, 8, 4)), (346348, 'NCT00999492', 'returned', 'August 20, 2014', datetime.date(2014, 8, 20)), (346349, 'NCT00999492', 'submitted', 'August 28, 2014', datetime.date(2014, 8, 28)), (346350, 'NCT00999492', 'returned', 'September 5, 2014', datetime.date(2014, 9, 5)), (346351, 'NCT00997750', 'submitted', 'August 11, 2011', datetime.date(2011, 8, 11)), (346352, 'NCT00997750', 'submission_canceled', 'Unknown', None), (346353, 'NCT00997347', 'submitted', 'March 14, 2013', datetime.date(2013, 3, 14)), (346354, 'NCT00997347', 'returned', 'April 30, 2013', datetime.date(2013, 4, 30)), (346355, 'NCT00997087', 'submitted', 'April 10, 2018', datetime.date(2018, 4, 10)), (346356, 'NCT00997087', 'returned', 'May 11, 2018', datetime.date(2018, 5, 11)), (346357, 'NCT00996866', 'submitted', 'May 17, 2016', datetime.date(2016, 5, 17)), (346358, 'NCT00996866', 'returned', 'June 24, 2016', datetime.date(2016, 6, 24)), (346359, 'NCT00996866', 'submitted', 'December 5, 2016', datetime.date(2016, 12, 5)), (346360, 'NCT00996866', 'returned', 'January 30, 2017', datetime.date(2017, 1, 30)), (346361, 'NCT00996385', 'submitted', 'October 15, 2019', datetime.date(2019, 10, 15)), (346362, 'NCT00996385', 'returned', 'November 1, 2019', datetime.date(2019, 11, 1)), (346363, 'NCT00995397', 'submitted', 'November 2, 2010', datetime.date(2010, 11, 2)), (346364, 'NCT00995397', 'returned', 'December 1, 2010', datetime.date(2010, 12, 1)), (346365, 'NCT00994734', 'submitted', 'March 18, 2013', datetime.date(2013, 3, 18)), (346366, 'NCT00994734', 'returned', 'May 15, 2013', datetime.date(2013, 5, 15)), (346367, 'NCT00994162', 'submitted', 'March 30, 2020', datetime.date(2020, 3, 30)), (346368, 'NCT00994162', 'returned', 'April 10, 2020', datetime.date(2020, 4, 10)), (346369, 'NCT00993759', 'submitted', 'February 7, 2012', datetime.date(2012, 2, 7)), (346370, 'NCT00993759', 'returned', 'March 7, 2012', datetime.date(2012, 3, 7)), (346371, 'NCT00993759', 'submitted', 'March 7, 2012', datetime.date(2012, 3, 7)), (346372, 'NCT00993759', 'returned', 'April 3, 2012', datetime.date(2012, 4, 3)), (346373, 'NCT00993707', 'submitted', 'December 26, 2020', datetime.date(2020, 12, 26)), (346374, 'NCT00993707', 'returned', 'January 20, 2021', datetime.date(2021, 1, 20)), (346375, 'NCT00993252', 'submitted', 'November 2, 2020', datetime.date(2020, 11, 2)), (346376, 'NCT00993252', 'returned', 'November 24, 2020', datetime.date(2020, 11, 24)), (346377, 'NCT00993070', 'submitted', 'April 24, 2017', datetime.date(2017, 4, 24)), (346378, 'NCT00993070', 'returned', 'August 2, 2017', datetime.date(2017, 8, 2)), (346379, 'NCT00992771', 'submitted', 'July 23, 2012', datetime.date(2012, 7, 23)), (346380, 'NCT00992771', 'returned', 'August 24, 2012', datetime.date(2012, 8, 24)), (346381, 'NCT00992771', 'submitted', 'December 7, 2012', datetime.date(2012, 12, 7)), (346382, 'NCT00992771', 'returned', 'January 14, 2013', datetime.date(2013, 1, 14)), (346383, 'NCT00992771', 'submitted', 'January 15, 2013', datetime.date(2013, 1, 15)), (346384, 'NCT00992771', 'returned', 'February 14, 2013', datetime.date(2013, 2, 14)), (346385, 'NCT00992771', 'submitted', 'December 15, 2014', datetime.date(2014, 12, 15)), (346386, 'NCT00992771', 'returned', 'December 24, 2014', datetime.date(2014, 12, 24)), (346387, 'NCT00992771', 'submitted', 'April 7, 2018', datetime.date(2018, 4, 7)), (346388, 'NCT00992771', 'returned', 'May 4, 2018', datetime.date(2018, 5, 4)), (346389, 'NCT00992667', 'submitted', 'February 24, 2011', datetime.date(2011, 2, 24)), (346390, 'NCT00992667', 'returned', 'March 23, 2011', datetime.date(2011, 3, 23)), (346391, 'NCT00992667', 'submitted', 'March 11, 2019', datetime.date(2019, 3, 11)), (346392, 'NCT00992667', 'returned', 'June 20, 2019', datetime.date(2019, 6, 20)), (346393, 'NCT00992160', 'submitted', 'February 24, 2017', datetime.date(2017, 2, 24)), (346394, 'NCT00992160', 'returned', 'April 7, 2017', datetime.date(2017, 4, 7)), (346395, 'NCT00992160', 'submitted', 'April 21, 2017', datetime.date(2017, 4, 21)), (346396, 'NCT00992160', 'returned', 'August 2, 2017', datetime.date(2017, 8, 2)), (346397, 'NCT00992160', 'submitted', 'September 5, 2017', datetime.date(2017, 9, 5)), (346398, 'NCT00992160', 'returned', 'April 5, 2018', datetime.date(2018, 4, 5)), (346399, 'NCT00992160', 'submitted', 'May 7, 2018', datetime.date(2018, 5, 7)), (346400, 'NCT00992160', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346401, 'NCT00991835', 'submitted', 'March 22, 2017', datetime.date(2017, 3, 22)), (346402, 'NCT00991835', 'returned', 'May 1, 2017', datetime.date(2017, 5, 1)), (346403, 'NCT00991835', 'submitted', 'May 1, 2017', datetime.date(2017, 5, 1)), (346404, 'NCT00991835', 'submission_canceled', 'Unknown', None), (346405, 'NCT00991835', 'submitted', 'August 22, 2017', datetime.date(2017, 8, 22)), (346406, 'NCT00991835', 'returned', 'March 15, 2018', datetime.date(2018, 3, 15)), (346407, 'NCT00991835', 'submitted', 'August 8, 2018', datetime.date(2018, 8, 8)), (346408, 'NCT00991835', 'returned', 'January 17, 2019', datetime.date(2019, 1, 17)), (346409, 'NCT00991835', 'submitted', 'February 25, 2019', datetime.date(2019, 2, 25)), (346410, 'NCT00991835', 'returned', 'June 4, 2019', datetime.date(2019, 6, 4)), (346411, 'NCT00991835', 'submitted', 'August 9, 2019', datetime.date(2019, 8, 9)), (346412, 'NCT00991835', 'submission_canceled', 'August 25, 2019', datetime.date(2019, 8, 25)), (346413, 'NCT00991835', 'submitted', 'August 25, 2019', datetime.date(2019, 8, 25)), (346414, 'NCT00991835', 'returned', 'September 25, 2019', datetime.date(2019, 9, 25)), (346415, 'NCT00991835', 'submitted', 'October 26, 2019', datetime.date(2019, 10, 26)), (346416, 'NCT00991835', 'returned', 'November 14, 2019', datetime.date(2019, 11, 14)), (346417, 'NCT00991731', 'submitted', 'April 17, 2017', datetime.date(2017, 4, 17)), (346418, 'NCT00991731', 'returned', 'June 28, 2017', datetime.date(2017, 6, 28)), (346419, 'NCT00989716', 'submitted', 'September 2, 2014', datetime.date(2014, 9, 2)), (346420, 'NCT00989716', 'returned', 'September 9, 2014', datetime.date(2014, 9, 9)), (346421, 'NCT00989716', 'submitted', 'February 4, 2016', datetime.date(2016, 2, 4)), (346422, 'NCT00989716', 'returned', 'March 3, 2016', datetime.date(2016, 3, 3)), (346423, 'NCT00988936', 'submitted', 'July 16, 2013', datetime.date(2013, 7, 16)), (346424, 'NCT00988936', 'submission_canceled', 'Unknown', None), (346425, 'NCT00988936', 'submitted', 'July 26, 2013', datetime.date(2013, 7, 26)), (346426, 'NCT00988936', 'returned', 'September 26, 2013', datetime.date(2013, 9, 26)), (346427, 'NCT00986466', 'submitted', 'May 18, 2015', datetime.date(2015, 5, 18)), (346428, 'NCT00986466', 'returned', 'June 10, 2015', datetime.date(2015, 6, 10)), (346429, 'NCT00986466', 'submitted', 'December 1, 2015', datetime.date(2015, 12, 1)), (346430, 'NCT00986466', 'returned', 'January 5, 2016', datetime.date(2016, 1, 5)), (346431, 'NCT00986466', 'submitted', 'May 12, 2016', datetime.date(2016, 5, 12)), (346432, 'NCT00986466', 'returned', 'June 21, 2016', datetime.date(2016, 6, 21)), (346433, 'NCT00986167', 'submitted', 'February 14, 2012', datetime.date(2012, 2, 14)), (346434, 'NCT00986167', 'returned', 'March 15, 2012', datetime.date(2012, 3, 15)), (346435, 'NCT00986167', 'submitted', 'February 9, 2015', datetime.date(2015, 2, 9)), (346436, 'NCT00986167', 'returned', 'February 25, 2015', datetime.date(2015, 2, 25)), (346437, 'NCT00985634', 'submitted', 'July 29, 2011', datetime.date(2011, 7, 29)), (346438, 'NCT00985634', 'returned', 'August 29, 2011', datetime.date(2011, 8, 29)), (346439, 'NCT00985634', 'submitted', 'October 10, 2012', datetime.date(2012, 10, 10)), (346440, 'NCT00985634', 'returned', 'November 8, 2012', datetime.date(2012, 11, 8)), (346441, 'NCT00983788', 'submitted', 'September 21, 2015', datetime.date(2015, 9, 21)), (346442, 'NCT00983788', 'returned', 'October 16, 2015', datetime.date(2015, 10, 16)), (346443, 'NCT00983333', 'submitted', 'October 14, 2019', datetime.date(2019, 10, 14)), (346444, 'NCT00983333', 'returned', 'November 1, 2019', datetime.date(2019, 11, 1)), (346445, 'NCT00983112', 'submitted', 'June 3, 2015', datetime.date(2015, 6, 3)), (346446, 'NCT00983112', 'returned', 'June 17, 2015', datetime.date(2015, 6, 17)), (346447, 'NCT00983112', 'submitted', 'November 10, 2015', datetime.date(2015, 11, 10)), (346448, 'NCT00983112', 'returned', 'December 14, 2015', datetime.date(2015, 12, 14)), (346449, 'NCT00983112', 'submitted', 'May 27, 2016', datetime.date(2016, 5, 27)), (346450, 'NCT00983112', 'returned', 'July 6, 2016', datetime.date(2016, 7, 6)), (346451, 'NCT00981773', 'submitted', 'October 16, 2019', datetime.date(2019, 10, 16)), (346452, 'NCT00981773', 'returned', 'November 6, 2019', datetime.date(2019, 11, 6)), (346458, 'NCT00980707', 'submitted', 'July 13, 2012', datetime.date(2012, 7, 13)), (346459, 'NCT00980707', 'submission_canceled', 'Unknown', None), (346460, 'NCT00980707', 'submitted', 'July 20, 2012', datetime.date(2012, 7, 20)), (346461, 'NCT00980707', 'submission_canceled', 'Unknown', None), (346462, 'NCT00979797', 'submitted', 'June 2, 2018', datetime.date(2018, 6, 2)), (346463, 'NCT00979797', 'returned', 'December 28, 2018', datetime.date(2018, 12, 28)), (346471, 'NCT00979563', 'submitted', 'May 15, 2015', datetime.date(2015, 5, 15)), (346472, 'NCT00979563', 'returned', 'June 1, 2015', datetime.date(2015, 6, 1)), (346473, 'NCT00978874', 'submitted', 'September 23, 2020', datetime.date(2020, 9, 23)), (346474, 'NCT00978874', 'returned', 'October 16, 2020', datetime.date(2020, 10, 16)), (346475, 'NCT00978796', 'submitted', 'December 12, 2013', datetime.date(2013, 12, 12)), (346476, 'NCT00978796', 'returned', 'January 31, 2014', datetime.date(2014, 1, 31)), (346477, 'NCT00978796', 'submitted', 'May 19, 2014', datetime.date(2014, 5, 19)), (346478, 'NCT00978796', 'returned', 'June 19, 2014', datetime.date(2014, 6, 19)), (346479, 'NCT00978744', 'submitted', 'January 14, 2016', datetime.date(2016, 1, 14)), (346480, 'NCT00978744', 'returned', 'February 11, 2016', datetime.date(2016, 2, 11)), (346481, 'NCT00978744', 'submitted', 'August 12, 2016', datetime.date(2016, 8, 12)), (346482, 'NCT00978744', 'returned', 'October 6, 2016', datetime.date(2016, 10, 6)), (346483, 'NCT00977028', 'submitted', 'December 26, 2014', datetime.date(2014, 12, 26)), (346484, 'NCT00977028', 'returned', 'January 8, 2015', datetime.date(2015, 1, 8)), (346485, 'NCT00977028', 'submitted', 'July 18, 2015', datetime.date(2015, 7, 18)), (346486, 'NCT00977028', 'submission_canceled', 'Unknown', None), (346487, 'NCT00977028', 'submitted', 'July 19, 2015', datetime.date(2015, 7, 19)), (346488, 'NCT00977028', 'returned', 'July 27, 2015', datetime.date(2015, 7, 27)), (346489, 'NCT00976365', 'submitted', 'December 29, 2011', datetime.date(2011, 12, 29)), (346490, 'NCT00976365', 'submission_canceled', 'Unknown', None), (346491, 'NCT00976287', 'submitted', 'October 21, 2010', datetime.date(2010, 10, 21)), (346492, 'NCT00976287', 'returned', 'October 29, 2010', datetime.date(2010, 10, 29)), (346493, 'NCT00974441', 'submitted', 'September 10, 2009', datetime.date(2009, 9, 10)), (346494, 'NCT00974441', 'returned', 'October 14, 2009', datetime.date(2009, 10, 14)), (346495, 'NCT00974012', 'submitted', 'September 10, 2009', datetime.date(2009, 9, 10)), (346496, 'NCT00974012', 'returned', 'October 13, 2009', datetime.date(2009, 10, 13)), (346497, 'NCT00973050', 'submitted', 'September 9, 2009', datetime.date(2009, 9, 9)), (346498, 'NCT00973050', 'returned', 'October 9, 2009', datetime.date(2009, 10, 9)), (346499, 'NCT00972985', 'submitted', 'March 24, 2011', datetime.date(2011, 3, 24)), (346500, 'NCT00972985', 'returned', 'April 15, 2011', datetime.date(2011, 4, 15)), (346501, 'NCT00972985', 'submitted', 'April 26, 2011', datetime.date(2011, 4, 26)), (346502, 'NCT00972985', 'returned', 'May 23, 2011', datetime.date(2011, 5, 23)), (346503, 'NCT00972855', 'submitted', 'September 9, 2009', datetime.date(2009, 9, 9)), (346504, 'NCT00972855', 'returned', 'October 9, 2009', datetime.date(2009, 10, 9)), (346505, 'NCT00972556', 'submitted', 'June 27, 2016', datetime.date(2016, 6, 27)), (346506, 'NCT00972556', 'returned', 'August 3, 2016', datetime.date(2016, 8, 3)), (346507, 'NCT00972556', 'submitted', 'August 4, 2016', datetime.date(2016, 8, 4)), (346508, 'NCT00972556', 'returned', 'September 28, 2016', datetime.date(2016, 9, 28)), (346509, 'NCT00972270', 'submitted', 'May 3, 2013', datetime.date(2013, 5, 3)), (346510, 'NCT00972270', 'returned', 'June 20, 2013', datetime.date(2013, 6, 20)), (346511, 'NCT00969475', 'submitted', 'July 24, 2011', datetime.date(2011, 7, 24)), (346512, 'NCT00969475', 'returned', 'August 18, 2011', datetime.date(2011, 8, 18)), (346513, 'NCT00969475', 'submitted', 'August 20, 2011', datetime.date(2011, 8, 20)), (346514, 'NCT00969475', 'returned', 'September 26, 2011', datetime.date(2011, 9, 26)), (346515, 'NCT00969475', 'submitted', 'April 19, 2012', datetime.date(2012, 4, 19)), (346516, 'NCT00969475', 'returned', 'May 16, 2012', datetime.date(2012, 5, 16)), (346517, 'NCT00969475', 'submitted', 'May 18, 2012', datetime.date(2012, 5, 18)), (346518, 'NCT00969475', 'returned', 'June 20, 2012', datetime.date(2012, 6, 20)), (346519, 'NCT00969059', 'submitted', 'August 10, 2017', datetime.date(2017, 8, 10)), (346520, 'NCT00969059', 'returned', 'February 19, 2018', datetime.date(2018, 2, 19)), (346521, 'NCT00969059', 'submitted', 'March 8, 2018', datetime.date(2018, 3, 8)), (346522, 'NCT00969059', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346523, 'NCT00968994', 'submitted', 'February 6, 2017', datetime.date(2017, 2, 6)), (346524, 'NCT00968994', 'returned', 'March 24, 2017', datetime.date(2017, 3, 24)), (346525, 'NCT00968513', 'submitted', 'February 8, 2017', datetime.date(2017, 2, 8)), (346526, 'NCT00968513', 'returned', 'March 27, 2017', datetime.date(2017, 3, 27)), (346527, 'NCT00967304', 'submitted', 'April 26, 2017', datetime.date(2017, 4, 26)), (346528, 'NCT00967304', 'returned', 'August 3, 2017', datetime.date(2017, 8, 3)), (346529, 'NCT00967148', 'submitted', 'February 21, 2017', datetime.date(2017, 2, 21)), (346530, 'NCT00967148', 'returned', 'April 6, 2017', datetime.date(2017, 4, 6)), (346531, 'NCT00966381', 'submitted', 'June 12, 2012', datetime.date(2012, 6, 12)), (346532, 'NCT00966381', 'returned', 'July 13, 2012', datetime.date(2012, 7, 13)), (346533, 'NCT00966381', 'submitted', 'April 30, 2019', datetime.date(2019, 4, 30)), (346534, 'NCT00966381', 'returned', 'July 12, 2019', datetime.date(2019, 7, 12)), (346535, 'NCT00964600', 'submitted', 'February 20, 2011', datetime.date(2011, 2, 20)), (346536, 'NCT00964600', 'returned', 'March 16, 2011', datetime.date(2011, 3, 16)), (346537, 'NCT00964600', 'submitted', 'July 25, 2011', datetime.date(2011, 7, 25)), (346538, 'NCT00964600', 'returned', 'August 17, 2011', datetime.date(2011, 8, 17)), (346539, 'NCT00964600', 'submitted', 'August 18, 2011', datetime.date(2011, 8, 18)), (346540, 'NCT00964600', 'returned', 'September 20, 2011', datetime.date(2011, 9, 20)), (346541, 'NCT00964600', 'submitted', 'January 18, 2012', datetime.date(2012, 1, 18)), (346542, 'NCT00964600', 'returned', 'February 16, 2012', datetime.date(2012, 2, 16)), (346543, 'NCT00964600', 'submitted', 'May 16, 2014', datetime.date(2014, 5, 16)), (346544, 'NCT00964600', 'returned', 'June 17, 2014', datetime.date(2014, 6, 17)), (346545, 'NCT00964054', 'submitted', 'March 21, 2014', datetime.date(2014, 3, 21)), (346546, 'NCT00964054', 'returned', 'April 23, 2014', datetime.date(2014, 4, 23)), (346547, 'NCT00963846', 'submitted', 'September 8, 2016', datetime.date(2016, 9, 8)), (346548, 'NCT00963846', 'returned', 'October 27, 2016', datetime.date(2016, 10, 27)), (346549, 'NCT00963794', 'submitted', 'August 2, 2011', datetime.date(2011, 8, 2)), (346550, 'NCT00963794', 'returned', 'August 30, 2011', datetime.date(2011, 8, 30)), (346551, 'NCT00963794', 'submitted', 'August 31, 2011', datetime.date(2011, 8, 31)), (346552, 'NCT00963794', 'returned', 'September 30, 2011', datetime.date(2011, 9, 30)), (346553, 'NCT00962702', 'submitted', 'April 17, 2011', datetime.date(2011, 4, 17)), (346554, 'NCT00962702', 'returned', 'May 11, 2011', datetime.date(2011, 5, 11)), (346555, 'NCT00962702', 'submitted', 'October 2, 2012', datetime.date(2012, 10, 2)), (346556, 'NCT00962702', 'returned', 'October 30, 2012', datetime.date(2012, 10, 30)), (346557, 'NCT00962702', 'submitted', 'August 16, 2014', datetime.date(2014, 8, 16)), (346558, 'NCT00962702', 'submission_canceled', 'Unknown', None), (346559, 'NCT00962702', 'submitted', 'August 23, 2014', datetime.date(2014, 8, 23)), (346560, 'NCT00962702', 'returned', 'September 3, 2014', datetime.date(2014, 9, 3)), (346561, 'NCT00961922', 'submitted', 'February 21, 2017', datetime.date(2017, 2, 21)), (346562, 'NCT00961922', 'returned', 'April 5, 2017', datetime.date(2017, 4, 5)), (346563, 'NCT00961714', 'submitted', 'August 4, 2014', datetime.date(2014, 8, 4)), (346564, 'NCT00961714', 'returned', 'August 19, 2014', datetime.date(2014, 8, 19)), (346565, 'NCT00961714', 'submitted', 'August 19, 2014', datetime.date(2014, 8, 19)), (346566, 'NCT00961714', 'returned', 'August 28, 2014', datetime.date(2014, 8, 28)), (346567, 'NCT00961714', 'submitted', 'January 15, 2016', datetime.date(2016, 1, 15)), (346568, 'NCT00961714', 'returned', 'February 11, 2016', datetime.date(2016, 2, 11)), (346569, 'NCT00961389', 'submitted', 'May 26, 2014', datetime.date(2014, 5, 26)), (346570, 'NCT00961389', 'returned', 'June 29, 2014', datetime.date(2014, 6, 29)), (346571, 'NCT00961389', 'submitted', 'November 13, 2014', datetime.date(2014, 11, 13)), (346572, 'NCT00961389', 'returned', 'November 20, 2014', datetime.date(2014, 11, 20)), (346573, 'NCT00961389', 'submitted', 'November 21, 2014', datetime.date(2014, 11, 21)), (346574, 'NCT00961389', 'returned', 'December 2, 2014', datetime.date(2014, 12, 2)), (346575, 'NCT00961376', 'submitted', 'August 27, 2019', datetime.date(2019, 8, 27)), (346576, 'NCT00961376', 'returned', 'September 17, 2019', datetime.date(2019, 9, 17)), (346577, 'NCT00961207', 'submitted', 'March 17, 2014', datetime.date(2014, 3, 17)), (346578, 'NCT00961207', 'returned', 'April 18, 2014', datetime.date(2014, 4, 18)), (346579, 'NCT00961207', 'submitted', 'February 2, 2015', datetime.date(2015, 2, 2)), (346580, 'NCT00961207', 'returned', 'February 4, 2015', datetime.date(2015, 2, 4)), (346581, 'NCT00961207', 'submitted', 'February 25, 2016', datetime.date(2016, 2, 25)), (346582, 'NCT00961207', 'returned', 'March 25, 2016', datetime.date(2016, 3, 25)), (346584, 'NCT00960401', 'submitted', 'January 27, 2016', datetime.date(2016, 1, 27)), (346585, 'NCT00960401', 'returned', 'February 23, 2016', datetime.date(2016, 2, 23)), (346586, 'NCT00960401', 'submitted', 'May 22, 2016', datetime.date(2016, 5, 22)), (346587, 'NCT00960401', 'returned', 'June 28, 2016', datetime.date(2016, 6, 28)), (346588, 'NCT00960024', 'submitted', 'December 9, 2015', datetime.date(2015, 12, 9)), (346589, 'NCT00960024', 'returned', 'January 12, 2016', datetime.date(2016, 1, 12)), (346590, 'NCT00959062', 'submitted', 'December 16, 2016', datetime.date(2016, 12, 16)), (346591, 'NCT00959062', 'returned', 'February 9, 2017', datetime.date(2017, 2, 9)), (346592, 'NCT00958932', 'submitted', 'September 23, 2014', datetime.date(2014, 9, 23)), (346593, 'NCT00958932', 'returned', 'September 26, 2014', datetime.date(2014, 9, 26)), (346594, 'NCT00958932', 'submitted', 'October 6, 2015', datetime.date(2015, 10, 6)), (346595, 'NCT00958932', 'returned', 'November 4, 2015', datetime.date(2015, 11, 4)), (346596, 'NCT00958932', 'submitted', 'March 6, 2017', datetime.date(2017, 3, 6)), (346597, 'NCT00958932', 'returned', 'April 17, 2017', datetime.date(2017, 4, 17)), (346598, 'NCT00956462', 'submitted', 'January 10, 2015', datetime.date(2015, 1, 10)), (346599, 'NCT00956462', 'returned', 'January 20, 2015', datetime.date(2015, 1, 20)), (346600, 'NCT00956462', 'submitted', 'May 27, 2019', datetime.date(2019, 5, 27)), (346601, 'NCT00956462', 'returned', 'July 22, 2019', datetime.date(2019, 7, 22)), (346602, 'NCT00956384', 'submitted', 'July 9, 2020', datetime.date(2020, 7, 9)), (346603, 'NCT00956384', 'returned', 'July 24, 2020', datetime.date(2020, 7, 24)), (346604, 'NCT00955981', 'submitted', 'August 26, 2016', datetime.date(2016, 8, 26)), (346605, 'NCT00955981', 'returned', 'October 20, 2016', datetime.date(2016, 10, 20)), (346606, 'NCT00955981', 'submitted', 'March 20, 2017', datetime.date(2017, 3, 20)), (346607, 'NCT00955981', 'returned', 'April 27, 2017', datetime.date(2017, 4, 27)), (346608, 'NCT00955981', 'submitted', 'January 3, 2018', datetime.date(2018, 1, 3)), (346609, 'NCT00955981', 'returned', 'January 30, 2018', datetime.date(2018, 1, 30)), (346610, 'NCT00955630', 'submitted', 'May 31, 2013', datetime.date(2013, 5, 31)), (346611, 'NCT00955630', 'returned', 'July 31, 2013', datetime.date(2013, 7, 31)), (346612, 'NCT00955630', 'submitted', 'August 7, 2013', datetime.date(2013, 8, 7)), (346613, 'NCT00955630', 'returned', 'October 11, 2013', datetime.date(2013, 10, 11)), (346614, 'NCT00955630', 'submitted', 'June 13, 2014', datetime.date(2014, 6, 13)), (346615, 'NCT00955630', 'submission_canceled', 'Unknown', None), (346616, 'NCT00955630', 'submitted', 'September 23, 2014', datetime.date(2014, 9, 23)), (346617, 'NCT00955630', 'returned', 'September 23, 2014', datetime.date(2014, 9, 23)), (346618, 'NCT00955630', 'submitted', 'September 23, 2014', datetime.date(2014, 9, 23)), (346619, 'NCT00955630', 'returned', 'September 24, 2014', datetime.date(2014, 9, 24)), (346620, 'NCT00955630', 'submitted', 'June 9, 2015', datetime.date(2015, 6, 9)), (346621, 'NCT00955630', 'returned', 'June 11, 2015', datetime.date(2015, 6, 11)), (346622, 'NCT00955552', 'submitted', 'June 22, 2017', datetime.date(2017, 6, 22)), (346623, 'NCT00955552', 'returned', 'November 3, 2017', datetime.date(2017, 11, 3)), (346624, 'NCT00955552', 'submitted', 'March 15, 2018', datetime.date(2018, 3, 15)), (346625, 'NCT00955552', 'submission_canceled', 'August 12, 2018', datetime.date(2018, 8, 12)), (346626, 'NCT00955552', 'submitted', 'August 12, 2018', datetime.date(2018, 8, 12)), (346627, 'NCT00955552', 'returned', 'January 24, 2019', datetime.date(2019, 1, 24)), (346628, 'NCT00955409', 'submitted', 'December 17, 2014', datetime.date(2014, 12, 17)), (346629, 'NCT00955409', 'returned', 'December 30, 2014', datetime.date(2014, 12, 30)), (346630, 'NCT00954304', 'submitted', 'May 15, 2015', datetime.date(2015, 5, 15)), (346631, 'NCT00954304', 'returned', 'June 5, 2015', datetime.date(2015, 6, 5)), (346632, 'NCT00953784', 'submitted', 'April 5, 2011', datetime.date(2011, 4, 5)), (346633, 'NCT00953784', 'returned', 'April 28, 2011', datetime.date(2011, 4, 28)), (346634, 'NCT00953784', 'submitted', 'May 17, 2011', datetime.date(2011, 5, 17)), (346635, 'NCT00953784', 'returned', 'September 29, 2011', datetime.date(2011, 9, 29)), (346636, 'NCT00952770', 'submitted', 'July 29, 2013', datetime.date(2013, 7, 29)), (346637, 'NCT00952770', 'returned', 'September 26, 2013', datetime.date(2013, 9, 26)), (346638, 'NCT00950677', 'submitted', 'December 4, 2020', datetime.date(2020, 12, 4)), (346639, 'NCT00950677', 'returned', 'December 30, 2020', datetime.date(2020, 12, 30)), (346640, 'NCT00950508', 'submitted', 'April 24, 2017', datetime.date(2017, 4, 24)), (346641, 'NCT00950508', 'returned', 'July 19, 2017', datetime.date(2017, 7, 19)), (346642, 'NCT00949130', 'submitted', 'March 17, 2011', datetime.date(2011, 3, 17)), (346643, 'NCT00949130', 'submission_canceled', 'Unknown', None), (346644, 'NCT00949130', 'submitted', 'July 6, 2011', datetime.date(2011, 7, 6)), (346645, 'NCT00949130', 'submission_canceled', 'Unknown', None), (346646, 'NCT00948805', 'submitted', 'August 4, 2011', datetime.date(2011, 8, 4)), (346647, 'NCT00948805', 'returned', 'September 7, 2011', datetime.date(2011, 9, 7)), (346648, 'NCT00948194', 'submitted', 'January 22, 2021', datetime.date(2021, 1, 22)), (346649, 'NCT00947375', 'submitted', 'August 10, 2009', datetime.date(2009, 8, 10)), (346650, 'NCT00947375', 'returned', 'September 4, 2009', datetime.date(2009, 9, 4)), (346651, 'NCT00947375', 'submitted', 'June 7, 2010', datetime.date(2010, 6, 7)), (346652, 'NCT00947375', 'returned', 'July 7, 2010', datetime.date(2010, 7, 7)), (346653, 'NCT00946556', 'submitted', 'September 6, 2016', datetime.date(2016, 9, 6)), (346654, 'NCT00946556', 'returned', 'October 26, 2016', datetime.date(2016, 10, 26)), (346655, 'NCT00946400', 'submitted', 'November 19, 2020', datetime.date(2020, 11, 19)), (346656, 'NCT00946400', 'returned', 'December 16, 2020', datetime.date(2020, 12, 16)), (346657, 'NCT00945932', 'submitted', 'July 28, 2017', datetime.date(2017, 7, 28)), (346658, 'NCT00945932', 'returned', 'February 16, 2018', datetime.date(2018, 2, 16)), (346659, 'NCT00945932', 'submitted', 'March 5, 2018', datetime.date(2018, 3, 5)), (346660, 'NCT00945932', 'submission_canceled', 'August 15, 2018', datetime.date(2018, 8, 15)), (346661, 'NCT00945568', 'submitted', 'June 6, 2012', datetime.date(2012, 6, 6)), (346662, 'NCT00945568', 'returned', 'July 10, 2012', datetime.date(2012, 7, 10)), (346663, 'NCT00944957', 'submitted', 'August 9, 2011', datetime.date(2011, 8, 9)), (346664, 'NCT00944957', 'returned', 'September 12, 2011', datetime.date(2011, 9, 12)), (346665, 'NCT00944957', 'submitted', 'September 15, 2011', datetime.date(2011, 9, 15)), (346666, 'NCT00944957', 'returned', 'October 24, 2011', datetime.date(2011, 10, 24)), (346667, 'NCT00944957', 'submitted', 'October 25, 2011', datetime.date(2011, 10, 25)), (346668, 'NCT00944957', 'returned', 'November 28, 2011', datetime.date(2011, 11, 28)), (346669, 'NCT00944216', 'submitted', 'August 4, 2011', datetime.date(2011, 8, 4)), (346670, 'NCT00944216', 'returned', 'September 7, 2011', datetime.date(2011, 9, 7)), (346671, 'NCT00944216', 'submitted', 'September 12, 2011', datetime.date(2011, 9, 12)), (346672, 'NCT00944216', 'returned', 'October 14, 2011', datetime.date(2011, 10, 14)), (346673, 'NCT00944216', 'submitted', 'November 1, 2011', datetime.date(2011, 11, 1)), (346674, 'NCT00944216', 'returned', 'December 2, 2011', datetime.date(2011, 12, 2)), (346675, 'NCT00944216', 'submitted', 'December 15, 2011', datetime.date(2011, 12, 15)), (346676, 'NCT00944216', 'returned', 'January 12, 2012', datetime.date(2012, 1, 12)), (346677, 'NCT00944190', 'submitted', 'September 11, 2019', datetime.date(2019, 9, 11)), (346678, 'NCT00944190', 'returned', 'October 1, 2019', datetime.date(2019, 10, 1)), (346679, 'NCT00943904', 'submitted', 'May 25, 2017', datetime.date(2017, 5, 25)), (346680, 'NCT00943904', 'returned', 'June 20, 2017', datetime.date(2017, 6, 20)), (346681, 'NCT00943904', 'submitted', 'February 5, 2018', datetime.date(2018, 2, 5)), (346682, 'NCT00943904', 'returned', 'March 6, 2018', datetime.date(2018, 3, 6)), (346683, 'NCT00943475', 'submitted', 'April 25, 2012', datetime.date(2012, 4, 25)), (346684, 'NCT00943475', 'returned', 'May 23, 2012', datetime.date(2012, 5, 23)), (346685, 'NCT00943475', 'submitted', 'September 6, 2012', datetime.date(2012, 9, 6)), (346686, 'NCT00943475', 'returned', 'October 4, 2012', datetime.date(2012, 10, 4)), (346687, 'NCT00943475', 'submitted', 'February 22, 2013', datetime.date(2013, 2, 22)), (346688, 'NCT00943475', 'returned', 'March 29, 2013', datetime.date(2013, 3, 29)), (346689, 'NCT00943475', 'submitted', 'March 10, 2017', datetime.date(2017, 3, 10)), (346690, 'NCT00943475', 'returned', 'April 20, 2017', datetime.date(2017, 4, 20)), (346691, 'NCT00943267', 'submitted', 'June 25, 2018', datetime.date(2018, 6, 25)), (346692, 'NCT00943267', 'returned', 'January 7, 2019', datetime.date(2019, 1, 7)), (346693, 'NCT00942305', 'submitted', 'December 9, 2020', datetime.date(2020, 12, 9)), (346694, 'NCT00942305', 'returned', 'January 4, 2021', datetime.date(2021, 1, 4)), (346695, 'NCT00942201', 'submitted', 'June 23, 2011', datetime.date(2011, 6, 23)), (346696, 'NCT00942201', 'returned', 'July 22, 2011', datetime.date(2011, 7, 22)), (346697, 'NCT00941941', 'submitted', 'November 2, 2009', datetime.date(2009, 11, 2)), (346698, 'NCT00941941', 'returned', 'December 1, 2009', datetime.date(2009, 12, 1)), (346699, 'NCT00941382', 'submitted', 'July 29, 2011', datetime.date(2011, 7, 29)), (346700, 'NCT00941382', 'returned', 'August 29, 2011', datetime.date(2011, 8, 29)), (346701, 'NCT00941382', 'submitted', 'September 2, 2011', datetime.date(2011, 9, 2)), (346702, 'NCT00941382', 'returned', 'October 5, 2011', datetime.date(2011, 10, 5)), (346703, 'NCT00941382', 'submitted', 'February 27, 2012', datetime.date(2012, 2, 27)), (346704, 'NCT00941382', 'returned', 'March 27, 2012', datetime.date(2012, 3, 27)), (346705, 'NCT00941382', 'submitted', 'July 20, 2012', datetime.date(2012, 7, 20)), (346706, 'NCT00941382', 'returned', 'August 22, 2012', datetime.date(2012, 8, 22)), (346707, 'NCT00940797', 'submitted', 'April 15, 2016', datetime.date(2016, 4, 15)), (346708, 'NCT00940797', 'returned', 'May 20, 2016', datetime.date(2016, 5, 20)), (346709, 'NCT00940407', 'submitted', 'October 22, 2012', datetime.date(2012, 10, 22)), (346710, 'NCT00940407', 'returned', 'November 20, 2012', datetime.date(2012, 11, 20)), (346711, 'NCT00940407', 'submitted', 'April 22, 2013', datetime.date(2013, 4, 22)), (346712, 'NCT00940407', 'returned', 'May 23, 2013', datetime.date(2013, 5, 23)), (346713, 'NCT00940368', 'submitted', 'April 13, 2010', datetime.date(2010, 4, 13)), (346714, 'NCT00940368', 'returned', 'April 28, 2010', datetime.date(2010, 4, 28)), (346715, 'NCT00938691', 'submitted', 'January 31, 2020', datetime.date(2020, 1, 31)), (346716, 'NCT00938691', 'returned', 'February 11, 2020', datetime.date(2020, 2, 11)), (346717, 'NCT00938691', 'submitted', 'October 13, 2020', datetime.date(2020, 10, 13)), (346718, 'NCT00938691', 'returned', 'November 4, 2020', datetime.date(2020, 11, 4)), (346719, 'NCT00937261', 'submitted', 'June 19, 2013', datetime.date(2013, 6, 19)), (346720, 'NCT00937261', 'returned', 'September 3, 2013', datetime.date(2013, 9, 3)), (346721, 'NCT00937261', 'submitted', 'January 25, 2017', datetime.date(2017, 1, 25)), (346722, 'NCT00937261', 'returned', 'March 14, 2017', datetime.date(2017, 3, 14)), (346723, 'NCT00937261', 'submitted', 'January 20, 2021', datetime.date(2021, 1, 20)), (346724, 'NCT00937261', 'returned', 'January 21, 2021', datetime.date(2021, 1, 21)), (346732, 'NCT00934895', 'submitted', 'March 31, 2017', datetime.date(2017, 3, 31)), (346733, 'NCT00934895', 'returned', 'May 10, 2017', datetime.date(2017, 5, 10)), (346734, 'NCT00934700', 'submitted', 'March 20, 2019', datetime.date(2019, 3, 20)), (346735, 'NCT00934700', 'returned', 'June 19, 2019', datetime.date(2019, 6, 19)), (346736, 'NCT00934700', 'submitted', 'August 6, 2019', datetime.date(2019, 8, 6)), (346737, 'NCT00934700', 'returned', 'September 11, 2019', datetime.date(2019, 9, 11)), (346738, 'NCT00933634', 'submitted', 'July 14, 2009', datetime.date(2009, 7, 14)), (346739, 'NCT00933634', 'returned', 'July 29, 2010', datetime.date(2010, 7, 29)), (346740, 'NCT00932854', 'submitted', 'October 31, 2017', datetime.date(2017, 10, 31)), (346741, 'NCT00932854', 'returned', 'August 7, 2018', datetime.date(2018, 8, 7)), (346742, 'NCT00932438', 'submitted', 'June 23, 2017', datetime.date(2017, 6, 23)), (346743, 'NCT00932438', 'returned', 'July 20, 2017', datetime.date(2017, 7, 20)), (346744, 'NCT00932100', 'submitted', 'May 29, 2013', datetime.date(2013, 5, 29)), (346745, 'NCT00932100', 'returned', 'July 25, 2013', datetime.date(2013, 7, 25)), (346746, 'NCT00931892', 'submitted', 'February 21, 2020', datetime.date(2020, 2, 21)), (346747, 'NCT00931892', 'returned', 'March 5, 2020', datetime.date(2020, 3, 5)), (346748, 'NCT00930943', 'submitted', 'April 19, 2012', datetime.date(2012, 4, 19)), (346749, 'NCT00930943', 'returned', 'May 17, 2012', datetime.date(2012, 5, 17)), (346750, 'NCT00930943', 'submitted', 'May 17, 2012', datetime.date(2012, 5, 17)), (346751, 'NCT00930943', 'returned', 'June 19, 2012', datetime.date(2012, 6, 19)), (346752, 'NCT00930943', 'submitted', 'August 30, 2017', datetime.date(2017, 8, 30)), (346753, 'NCT00930943', 'returned', 'September 26, 2017', datetime.date(2017, 9, 26)), (346754, 'NCT00930579', 'submitted', 'June 15, 2017', datetime.date(2017, 6, 15)), (346755, 'NCT00930579', 'returned', 'July 14, 2017', datetime.date(2017, 7, 14)), (346756, 'NCT00929253', 'submitted', 'January 15, 2019', datetime.date(2019, 1, 15)), (346757, 'NCT00929253', 'returned', 'February 5, 2019', datetime.date(2019, 2, 5)), (346758, 'NCT00929097', 'submitted', 'May 22, 2013', datetime.date(2013, 5, 22)), (346759, 'NCT00929097', 'returned', 'August 27, 2013', datetime.date(2013, 8, 27)), (346760, 'NCT00928876', 'submitted', 'April 14, 2011', datetime.date(2011, 4, 14)), (346761, 'NCT00928876', 'returned', 'May 9, 2011', datetime.date(2011, 5, 9)), (346762, 'NCT00928876', 'submitted', 'October 9, 2017', datetime.date(2017, 10, 9)), (346763, 'NCT00928876', 'returned', 'July 13, 2018', datetime.date(2018, 7, 13)), (346764, 'NCT00928811', 'submitted', 'September 15, 2016', datetime.date(2016, 9, 15)), (346765, 'NCT00928811', 'returned', 'November 1, 2016', datetime.date(2016, 11, 1)), (346766, 'NCT00928811', 'submitted', 'July 25, 2017', datetime.date(2017, 7, 25)), (346767, 'NCT00928811', 'returned', 'August 24, 2017', datetime.date(2017, 8, 24)), (346775, 'NCT00928499', 'submitted', 'July 23, 2013', datetime.date(2013, 7, 23)), (346776, 'NCT00928499', 'returned', 'September 24, 2013', datetime.date(2013, 9, 24)), (346777, 'NCT00928499', 'submitted', 'May 25, 2017', datetime.date(2017, 5, 25)), (346778, 'NCT00928499', 'returned', 'June 27, 2017', datetime.date(2017, 6, 27)), (346779, 'NCT00928499', 'submitted', 'February 5, 2018', datetime.date(2018, 2, 5)), (346780, 'NCT00928499', 'returned', 'March 6, 2018', datetime.date(2018, 3, 6)), (346781, 'NCT00928135', 'submitted', 'October 27, 2020', datetime.date(2020, 10, 27)), (346782, 'NCT00928135', 'returned', 'November 18, 2020', datetime.date(2020, 11, 18)), (346783, 'NCT00927381', 'submitted', 'July 1, 2014', datetime.date(2014, 7, 1)), (346784, 'NCT00927381', 'returned', 'July 30, 2014', datetime.date(2014, 7, 30)), (346785, 'NCT00927381', 'submitted', 'September 9, 2014', datetime.date(2014, 9, 9)), (346786, 'NCT00927381', 'returned', 'September 16, 2014', datetime.date(2014, 9, 16))]
# # id,nct_id,event,event_date_description,event_date
# # print(aa)
# d ={}
# for i in aa:
#     nct_id = i[1]
#     dd = {}
#     dd['id'] = i[0]
#     dd['event'] = i[2]
#     dd['event_date_description'] = i[3]
#     dd['event_date'] = i[4]
#     d.setdefault(nct_id, []).append(dd)
#
#     # d[nct_id] = dd
#     # if nct_id not in d:
#     #     list = []
#     #     list.append(dd)
#     #     d[nct_id] = list
#     # else:
#     #     d[nct_id] = d[nct_id].append(dd)
# print(d)
cc = {}
aa = {'NCT00918060': [{'id': 346836,'event': 'submitted'}],'NCT00918061': [{'id': 346837,'event': 'submitted'}]}
bb = {'NCT00918061': [{'id': 346838,'event': 'submitted'}],'NCT00918062': [{'id': 346839,'event': 'submitted'}]}
"""
for key in aa:
    # print(key)
    if bb.get(key):
        cc[key] = aa[key]+bb[key]
        del bb[key]
        cc.update(bb)
    elif aa.get(key):
        cc[key] = aa[key]
# """
# cc.update(aa)
# cc.update(bb)
# print(cc)


# aa = "2020-03-25"
# print(aa)
# print(aa.replace("-",''))
# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据# 读数据

"""
print(type(d))
for i in d:
    ll = d[i]
    for j in ll:
        print(j['id'])
"""


"""
dd = {}
    if nct_id not in dd.keys():
        dd[nct_id] = 1
    else:
        dd[nct_id] = dd[nct_id] + 1
print(dd)
"""

# 获取数据
# n = 0
# dic = {}
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         print(i)
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['document_id'] = i[2]
#         dd['document_type'] = i[3]
#         dd['url'] = i[4]
#         dd['comment'] = i[5]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
# print(dic)
# print(len(dic))

# cursor1.execute("SELECT * FROM categories")
# while True:
#     data = cursor1.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['name'] = i[2]
#         dd['created_at'] = i[3]
#         dd['updated_at'] = i[4]
#         dd['grouping'] = i[5]
#         dd['study_search_id'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
# print(dic)
# print(len(dic))
#
# cursor.execute("SELECT * FROM study_references")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['pmid'] = i[2]
#         dd['reference_type'] = i[3]
#         dd['citation'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM studies")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[0]
#         dd = {}
#         dd['nlm_download_date_description'] = i[1]
#         dd['study_first_submitted_date'] = i[2]
#         dd['results_first_submitted_date'] = i[3]
#         dd['disposition_first_submitted_date'] = i[4]
#         dd['last_update_submitted_date'] = i[5]
#         dd['study_first_submitted_qc_date'] = i[6]
#         dd['study_first_posted_date'] = i[7]
#         dd['study_first_posted_date_type'] = i[8]
#         dd['results_first_submitted_qc_date'] = i[9]
#         dd['results_first_posted_date'] = i[10]
#         dd['results_first_posted_date_type'] = i[11]
#         dd['disposition_first_submitted_qc_date'] = i[12]
#         dd['disposition_first_posted_date'] = i[13]
#         dd['disposition_first_posted_date_type'] = i[14]
#         dd['last_update_submitted_qc_date'] = i[15]
#         dd['last_update_posted_date'] = i[16]
#         dd['last_update_posted_date_type'] = i[17]
#         dd['start_month_year'] = i[18]
#         dd['start_date_type'] = i[19]
#         dd['start_date'] = i[20]
#         dd['verification_month_year'] = i[21]
#         dd['verification_date'] = i[22]
#         dd['completion_month_year'] = i[23]
#         dd['completion_date_type'] = i[24]
#         dd['completion_date'] = i[25]
#         dd['primary_completion_month_year'] = i[26]
#         dd['primary_completion_date_type'] = i[27]
#         dd['primary_completion_date'] = i[28]
#         dd['target_duration'] = i[29]
#         dd['study_type'] = i[30]
#         dd['acronym'] = i[31]
#         dd['baseline_population'] = i[32]
#         dd['brief_title'] = i[33]
#         dd['official_title'] = i[34]
#         dd['overall_status'] = i[35]
#         dd['last_known_status'] = i[36]
#         dd['phase'] = i[37]
#         dd['enrollment'] = i[38]
#         dd['enrollment_type'] = i[39]
#         dd['source'] = i[40]
#         dd['limitations_and_caveats'] = i[41]
#         dd['number_of_arms'] = i[42]
#         dd['number_of_groups'] = i[43]
#         dd['why_stopped'] = i[44]
#         dd['has_expanded_access'] = i[45]
#         dd['expanded_access_type_individual'] = i[46]
#         dd['expanded_access_type_intermediate'] = i[47]
#         dd['expanded_access_type_treatment'] = i[48]
#         dd['has_dmc'] = i[49]
#         dd['is_fda_regulated_drug'] = i[50]
#         dd['is_fda_regulated_device'] = i[51]
#         dd['is_unapproved_device'] = i[52]
#         dd['is_ppsd'] = i[53]
#         dd['is_us_export'] = i[54]
#         dd['biospec_retention'] = i[55]
#         dd['biospec_description'] = i[56]
#         dd['ipd_time_frame'] = i[57]
#         dd['ipd_access_criteria'] = i[58]
#         dd['ipd_url'] = i[59]
#         dd['plan_to_share_ipd'] = i[60]
#         dd['plan_to_share_ipd_description'] = i[61]
#         dd['created_at'] = i[62]
#         dd['updated_at'] = i[63]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM sponsors")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['agency_class'] = i[2]
#         dd['lead_or_collaborator'] = i[3]
#         dd['name'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM result_groups")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['ctgov_group_code'] = i[2]
#         dd['result_type'] = i[3]
#         dd['title'] = i[4]
#         dd['description'] = i[5]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM result_agreements")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['pi_employee'] = i[2]
#         dd['agreement'] = i[3]
#         dd['restriction_type'] = i[4]
#         dd['other_details'] = i[5]
#         dd['restrictive_agreement'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM responsible_parties")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['responsible_party_type'] = i[2]
#         dd['name'] = i[3]
#         dd['title'] = i[4]
#         dd['organization'] = i[5]
#         dd['affiliation'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM reported_events")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['result_group_id'] = i[2]
#         dd['ctgov_group_code'] = i[3]
#         dd['time_frame'] = i[4]
#         dd['event_type'] = i[5]
#         dd['default_vocab'] = i[6]
#         dd['default_assessment'] = i[7]
#         dd['subjects_affected'] = i[8]
#         dd['subjects_at_risk'] = i[9]
#         dd['description'] = i[10]
#         dd['event_count'] = i[11]
#         dd['organ_system'] = i[12]
#         dd['adverse_event_term'] = i[13]
#         dd['frequency_threshold'] = i[14]
#         dd['vocab'] = i[15]
#         dd['assessment'] = i[16]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM reported_events_totals")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['ctgov_group_code'] = i[2]
#         dd['event_type'] = i[3]
#         dd['classification'] = i[4]
#         dd['subjects_affected'] = i[5]
#         dd['subjects_at_risk'] = i[6]
#         dd['created_at'] = i[7]
#         dd['updated_at'] = i[8]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM provided_documents")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['document_type'] = i[2]
#         dd['has_protocol'] = i[3]
#         dd['has_icf'] = i[4]
#         dd['has_sap'] = i[5]
#         dd['document_date'] = i[6]
#         dd['url'] = i[7]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM pending_results")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['event'] = i[2]
#         dd['event_date_description'] = i[3]
#         dd['event_date'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM participant_flows")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['recruitment_details'] = i[2]
#         dd['pre_assignment_details'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM overall_officials")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['role'] = i[2]
#         dd['name'] = i[3]
#         dd['affiliation'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM outcomes")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['outcome_type'] = i[2]
#         dd['title'] = i[3]
#         dd['description'] = i[4]
#         dd['time_frame'] = i[5]
#         dd['population'] = i[6]
#         dd['anticipated_posting_date'] = i[7]
#         dd['anticipated_posting_month_year'] = i[8]
#         dd['units'] = i[9]
#         dd['units_analyzed'] = i[10]
#         dd['dispersion_type'] = i[11]
#         dd['param_type'] = i[12]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM outcome_measurements")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['outcome_id'] = i[2]
#         dd['result_group_id'] = i[3]
#         dd['ctgov_group_code'] = i[4]
#         dd['classification'] = i[5]
#         dd['category'] = i[6]
#         dd['title'] = i[7]
#         dd['description'] = i[8]
#         dd['units'] = i[9]
#         dd['param_type'] = i[10]
#         dd['param_value'] = i[11]
#         dd['param_value_num'] = i[12]
#         dd['dispersion_type'] = i[13]
#         dd['dispersion_value'] = i[14]
#         dd['dispersion_value_num'] = i[15]
#         dd['dispersion_lower_limit'] = i[16]
#         dd['dispersion_upper_limit'] = i[17]
#         dd['explanation_of_na'] = i[18]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM outcome_counts")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['outcome_id'] = i[2]
#         dd['result_group_id'] = i[3]
#         dd['ctgov_group_code'] = i[4]
#         dd['scope'] = i[5]
#         dd['units'] = i[6]
#         dd['count'] = i[7]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM outcome_analysis_groups")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['outcome_analysis_id'] = i[2]
#         dd['result_group_id'] = i[3]
#         dd['ctgov_group_code'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM outcome_analyses")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['outcome_id'] = i[2]
#         dd['non_inferiority_type'] = i[3]
#         dd['non_inferiority_description'] = i[4]
#         dd['param_type'] = i[5]
#         dd['param_value'] = i[6]
#         dd['dispersion_type'] = i[7]
#         dd['dispersion_value'] = i[8]
#         dd['p_value_modifier'] = i[9]
#         dd['p_value'] = i[10]
#         dd['ci_n_sides'] = i[11]
#         dd['ci_percent'] = i[12]
#         dd['ci_lower_limit'] = i[13]
#         dd['ci_upper_limit'] = i[14]
#         dd['ci_upper_limit_na_comment'] = i[15]
#         dd['p_value_description'] = i[16]
#         dd['method'] = i[17]
#         dd['method_description'] = i[18]
#         dd['estimate_description'] = i[19]
#         dd['groups_description'] = i[20]
#         dd['other_analysis_description'] = i[21]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM milestones")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['result_group_id'] = i[2]
#         dd['ctgov_group_code'] = i[3]
#         dd['title'] = i[4]
#         dd['period'] = i[5]
#         dd['description'] = i[6]
#         dd['count'] = i[7]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM links")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['url'] = i[2]
#         dd['description'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM keywords")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['name'] = i[2]
#         dd['downcase_name'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM ipd_information_types")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['name'] = i[2]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM interventions")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['intervention_type'] = i[2]
#         dd['name'] = i[3]
#         dd['description'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM intervention_other_names")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['intervention_id'] = i[2]
#         dd['name'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM id_information")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['id_type'] = i[2]
#         dd['id_value'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM facility_investigators")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['facility_id'] = i[2]
#         dd['role'] = i[3]
#         dd['name'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM facility_contacts")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['facility_id'] = i[2]
#         dd['contact_type'] = i[3]
#         dd['name'] = i[4]
#         dd['email'] = i[5]
#         dd['phone'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM facilities")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['status'] = i[2]
#         dd['name'] = i[3]
#         dd['city'] = i[4]
#         dd['state'] = i[5]
#         dd['zip'] = i[6]
#         dd['country'] = i[7]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM eligibilities")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['sampling_method'] = i[2]
#         dd['gender'] = i[3]
#         dd['minimum_age'] = i[4]
#         dd['maximum_age'] = i[5]
#         dd['healthy_volunteers'] = i[6]
#         dd['population'] = i[7]
#         dd['criteria'] = i[8]
#         dd['gender_description'] = i[9]
#         dd['gender_based'] = i[10]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM drop_withdrawals")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['result_group_id'] = i[2]
#         dd['ctgov_group_code'] = i[3]
#         dd['period'] = i[4]
#         dd['reason'] = i[5]
#         dd['count'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM documents")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['document_id'] = i[2]
#         dd['document_type'] = i[3]
#         dd['url'] = i[4]
#         dd['comment'] = i[5]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM detailed_descriptions")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['description'] = i[2]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM designs")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['allocation'] = i[2]
#         dd['intervention_model'] = i[3]
#         dd['observational_model'] = i[4]
#         dd['primary_purpose'] = i[5]
#         dd['time_perspective'] = i[6]
#         dd['masking'] = i[7]
#         dd['masking_description'] = i[8]
#         dd['intervention_model_description'] = i[9]
#         dd['subject_masked'] = i[10]
#         dd['caregiver_masked'] = i[11]
#         dd['investigator_masked'] = i[12]
#         dd['outcomes_assessor_masked'] = i[13]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM design_outcomes")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['outcome_type'] = i[2]
#         dd['measure'] = i[3]
#         dd['time_frame'] = i[4]
#         dd['population'] = i[5]
#         dd['description'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM design_groups")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['group_type'] = i[2]
#         dd['title'] = i[3]
#         dd['description'] = i[4]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM design_group_interventions")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['design_group_id'] = i[2]
#         dd['intervention_id'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM countries")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['name'] = i[2]
#         dd['removed'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM conditions")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['name'] = i[2]
#         dd['downcase_name'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM central_contacts")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['contact_type'] = i[2]
#         dd['name'] = i[3]
#         dd['phone'] = i[4]
#         dd['email'] = i[5]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM categories")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['name'] = i[2]
#         dd['created_at'] = i[3]
#         dd['updated_at'] = i[4]
#         dd['grouping'] = i[5]
#         dd['study_search_id'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM calculated_values")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['number_of_facilities'] = i[2]
#         dd['number_of_nsae_subjects'] = i[3]
#         dd['number_of_sae_subjects'] = i[4]
#         dd['registered_in_calendar_year'] = i[5]
#         dd['nlm_download_date'] = i[6]
#         dd['actual_duration'] = i[7]
#         dd['were_results_reported'] = i[8]
#         dd['months_to_report_results'] = i[9]
#         dd['has_us_facility'] = i[10]
#         dd['has_single_facility'] = i[11]
#         dd['minimum_age_num'] = i[12]
#         dd['maximum_age_num'] = i[13]
#         dd['minimum_age_unit'] = i[14]
#         dd['maximum_age_unit'] = i[15]
#         dd['number_of_primary_outcomes_to_measure'] = i[16]
#         dd['number_of_secondary_outcomes_to_measure'] = i[17]
#         dd['number_of_other_outcomes_to_measure'] = i[18]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM browse_interventions")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['mesh_term'] = i[2]
#         dd['downcase_mesh_term'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM browse_conditions")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['mesh_term'] = i[2]
#         dd['downcase_mesh_term'] = i[3]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM brief_summaries")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['description'] = i[2]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM baseline_measurements")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['result_group_id'] = i[2]
#         dd['ctgov_group_code'] = i[3]
#         dd['classification'] = i[4]
#         dd['category'] = i[5]
#         dd['title'] = i[6]
#         dd['description'] = i[7]
#         dd['units'] = i[8]
#         dd['param_type'] = i[9]
#         dd['has_us_facility'] = i[10]
#         dd['param_value_num'] = i[11]
#         dd['dispersion_type'] = i[12]
#         dd['dispersion_value'] = i[13]
#         dd['dispersion_value_num'] = i[14]
#         dd['dispersion_lower_limit'] = i[15]
#         dd['dispersion_upper_limit'] = i[16]
#         dd['explanation_of_na'] = i[17]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break
#
# cursor.execute("SELECT * FROM baseline_counts")
# while True:
#     data = cursor.fetchmany(1000)
#     d = {}
#     for i in data:
#         nct_id = i[1]
#         dd = {}
#         dd['id'] = i[0]
#         dd['result_group_id'] = i[2]
#         dd['ctgov_group_code'] = i[3]
#         dd['units'] = i[4]
#         dd['scope'] = i[5]
#         dd['count'] = i[6]
#         d.setdefault(nct_id, []).append(dd)
#     dic.update(d)
#     if data == []:
#         break