#!/bin/sh

# rocedu (http://www.cnblogs.com/rocedu)
# Wechat Public Number: rocedu

clear
echo "//=====Today:====================================="
echo "code summary infomation:"
find . -name "*.py" -mtime 0 | xargs cat | grep -v ^$ | wc -l 
find . -name "*.sh"| xargs cat | grep -v ^$ | wc -l 
echo "documents summary infomation:"
find . -name "*.md" -mtime 0 | xargs cat | grep -v ^$ | wc -l 
echo ""

echo "//=====This Week:================================="
echo "code summary infomation:"
find . -name "*.py" -mtime -7| xargs cat | grep -v ^$ | wc -l 
find . -name "*.sh"| xargs cat | grep -v ^$ | wc -l 
echo "documents summary infomation:"
find . -name "*.md" -mtime -7| xargs cat | grep -v ^$ | wc -l 
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-0 days"`
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-1 days"`
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-2 days"`
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-3 days"`
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-4 days"`
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-5 days"`
git log --pretty=format:"%h - %an,%ci: %s " | grep  `date +%F --date="-6 days"`
echo ""
echo ""

echo "//=====This Semester:=============================="
echo "code summary infomation:"
find . -name "*.py"| xargs cat | grep -v ^$ | wc -l 
find . -name "*.sh"| xargs cat | grep -v ^$ | wc -l 
echo "documents summary infomation:"
find . -name "*.md"| xargs cat | grep -v ^$ | wc -l 
echo "commit history:"
git log --pretty=format:"%h - %an,%ci: %s "
