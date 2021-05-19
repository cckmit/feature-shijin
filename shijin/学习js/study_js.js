'use strict';

// const co = require('co');
// const fs = require('fs');
// const Nightmare = require('nightmare'); // 可视化的浏览器
// const url = 'http://sports.qq.com/isocce/';
//
// const onError = function(err) {
//     console.log(err);
// };
//
// const getHtml = function(pageUrl) {
//     const pageScraper = new Nightmare(); // 打开浏览器
//     let content = null;
//
//     return co(function * run() {
//         yield pageScraper.goto(pageUrl.url).wait();
//         console.log('222222' + pageUrl.url);
//         content = yield pageScraper.evaluate(() = >{
//             const temp = document.querySelector('body').innerHTML;
//             return temp;
//         });
//         console.log('子页面链接');
//         console.dir(content);
//
//         yield fs.writeFile('../../saveFiles/' + pageUrl.title + '.html', content, (err) = >{
//             console.log('存文件.......');
//             if (err) return console.log(err);
//             return console.log('Save pageUrl content to ' + pageUrl.title + '.html');
//         });
//     });
// };
//
// co(function * run() {
//     const scraper = new Nightmare({
//         show: true
//     }); // 打开一个可视化的浏览器
//     let counter = 0;
//     // let next = null;
//     let links = [];
//
//     yield scraper.goto(url) // 跳转的地址
//     .wait();
//     // .click('#feed-laliga > a');
//     for (let i = 0; i < 5; i++) {
//         yield scraper.wait(2000).click('#feed-laliga > a');
//     }
//
//     links = yield scraper.evaluate(() = >{
//         const temp = document.querySelectorAll('#feed-laliga h3 > a');
//         const list = [];
//         for (const each of temp) {
//             console.log('each');
//             console.log(each);
//             list.push({
//                 title: each.innerText,
//                 url: each.href,
//             });
//         }
//         return list;
//     });
//     // 在这里 加载更多
//
//     console.log('这里');
//     console.dir(links);
//
//     for (const link of links) {
//         if (link !== null && link.url !== 'javascript:void(0)') {
//             counter += 1;
//             setTimeout(() = >{
//                 getHtml(link);
//             },
//             counter * links.length * 250);
//         }
//     }
//     yield scraper.end();
// }).
// catch(onError);