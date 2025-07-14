/*
 WanquanZhongwen - Based on the following.
 Michael Etzkorn.
 ---

 Zhongwen - A Chinese-English Pop-Up Dictionary
 Copyright (C) 2010-2019 Christian Schiller
 https://chrome.google.com/extensions/detail/kkmlkkjojmombglmlpbpapmhcaljjkde

 ---

 Originally based on Rikaikun 0.8
 Copyright (C) 2010 Erek Speed
 http://code.google.com/p/rikaikun/

 ---

 Originally based on Rikaichan 1.07
 by Jonathan Zarate
 http://www.polarcloud.com/

 ---

 Originally based on RikaiXUL 0.4 by Todd Rudick
 http://www.rikai.com/
 http://rikaixul.mozdev.org/

 ---

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

 ---

 Please do not change or remove any of the copyrights or links to web pages
 when modifying any of the files.

 */

'use strict';

import { ZhongwenDictionary } from './dict.js';

let dict;
let isActivated = false;

// Default options
const defaultOptions = {
    css: 'yellow',
    tonecolors: 'yes',
    fontSize: 'small',
    skritterTLD: 'com',
    zhuyin: 'no',
    grammar: 'yes',
    simpTrad: 'classic',
    toneColorScheme: 'standard',
    enabled: '1', // '1' for enabled, '0' for disabled
    wordlist: [],
    saveToWordList: 'allEntries'
};

// Function to get options from storage, providing defaults if not set
async function getOptions() {
    const storedOptions = await chrome.storage.local.get(Object.keys(defaultOptions));
    return { ...defaultOptions, ...storedOptions };
}

async function loadDictData() {
    const wordDictUrl = chrome.runtime.getURL("data/new_new_cedict_ts.u8.txt");
    const wordIndexUrl = chrome.runtime.getURL("data/multi_cedict.idx");
    const grammarKeywordsUrl = chrome.runtime.getURL("data/grammarKeywordsMin.json");

    const [wordDictRes, wordIndexRes, grammarKeywordsRes] = await Promise.all([
        fetch(wordDictUrl),
        fetch(wordIndexUrl),
        fetch(grammarKeywordsUrl)
    ]);

    const [wordDict, wordIndex, grammarKeywords] = await Promise.all([
        wordDictRes.text(),
        wordIndexRes.text(),
        grammarKeywordsRes.json()
    ]);

    return { wordDict, wordIndex, grammarKeywords };
}

async function getDictionary() {
    if (!dict) {
        const { wordDict, wordIndex, grammarKeywords } = await loadDictData();
        dict = new ZhongwenDictionary(wordDict, wordIndex, grammarKeywords);
    }
    return dict;
}

function updateIcon(enabled) {
    if (enabled) {
        chrome.action.setBadgeBackgroundColor({ color: [255, 0, 0, 255] });
        chrome.action.setBadgeText({ text: 'On' });
    } else {
        chrome.action.setBadgeBackgroundColor({ color: [0, 0, 0, 0] });
        chrome.action.setBadgeText({ text: '' });
    }
}

function setupContextMenus() {
    chrome.contextMenus.removeAll(() => {
        chrome.contextMenus.create({
            id: 'open-wordlist',
            title: 'Open word list',
            contexts: ['action']
        });
        chrome.contextMenus.create({
            id: 'show-help',
            title: 'Show help in new tab',
            contexts: ['action']
        });
    });
}

async function activateExtension(tabId, showHelp) {
    isActivated = true;
    await chrome.storage.local.set({ enabled: '1' });
    updateIcon(true);
    setupContextMenus();
    await getDictionary();

    const options = await getOptions();
    chrome.tabs.sendMessage(tabId, {
        type: 'enable',
        config: options
    }).catch(e => console.log("Could not enable tab:", e));

    if (showHelp) {
        chrome.tabs.sendMessage(tabId, { type: 'showHelp' }).catch(e => console.log("Could not show help:", e));
    }
}

async function deactivateExtension() {
    isActivated = false;
    await chrome.storage.local.set({ enabled: '0' });
    dict = null; // Allow dictionary to be garbage collected
    updateIcon(false);
    chrome.contextMenus.removeAll();

    const tabs = await chrome.tabs.query({});
    for (const tab of tabs) {
        // Ignore errors for tabs that can't be scripted
        chrome.tabs.sendMessage(tab.id, { type: 'disable' }).catch(() => {});
    }
}

async function enableTab(tabId) {
    const { enabled } = await getOptions();
    if (enabled === '1') {
        if (!isActivated) {
            isActivated = true;
            updateIcon(true);
            setupContextMenus();
        }
        const options = await getOptions();
        chrome.tabs.sendMessage(tabId, {
            type: 'enable',
            config: options
        }).catch(() => { /* Suppress errors for non-scriptable tabs */ });
    }
}

// Initialize extension state on startup
chrome.runtime.onInstalled.addListener(async () => {
    const { enabled } = await getOptions();
    if (enabled === '1') {
        isActivated = true;
        updateIcon(true);
        setupContextMenus();
    }
});

chrome.runtime.onStartup.addListener(async () => {
    const { enabled } = await getOptions();
    if (enabled === '1') {
        isActivated = true;
        updateIcon(true);
        setupContextMenus();
    }
});


// Main toggle action
chrome.action.onClicked.addListener(async (tab) => {
    const { enabled } = await getOptions();
    if (enabled === '1') {
        await deactivateExtension();
    } else {
        await activateExtension(tab.id, true);
    }
});

// Context menu actions
chrome.contextMenus.onClicked.addListener((info, tab) => {
    let page = 'help.html';
    if (info.menuItemId === 'open-wordlist') {
        page = 'wordlist.html';
    }
    const url = chrome.runtime.getURL(page);
    chrome.tabs.create({ url });
});

// Tab event listeners
chrome.tabs.onActivated.addListener(activeInfo => {
    enableTab(activeInfo.tabId);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
        enableTab(tabId);
    }
});

// Message listener for content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    (async () => {
        switch (request.type) {
            case 'search': {
                const dictionary = await getDictionary();
                if (!dictionary) {
                    sendResponse(null);
                    return;
                }
                let entry = dictionary.wordSearch(request.text);
                if (entry) {
                    for (let i = 0; i < entry.data.length; i++) {
                        let word = entry.data[i][1];
                        if (dictionary.hasKeyword(word) && (entry.matchLen === word.length)) {
                            entry.grammar = { keyword: word, index: i };
                        }
                    }
                    entry.originalText = request.originalText;
                }
                sendResponse(entry);
                break;
            }
            case 'open': {
                const url = request.url.startsWith('/') ? chrome.runtime.getURL(request.url.substring(1)) : request.url;
                const allTabs = await chrome.tabs.query({});
                const existingTab = allTabs.find(tab => tab.url === url);
                if (existingTab) {
                    chrome.tabs.update(existingTab.id, { active: true });
                } else {
                    chrome.tabs.create({ url });
                }
                break;
            }
            case 'copy': {
                if (sender.tab) {
                    chrome.scripting.executeScript({
                        target: { tabId: sender.tab.id },
                        func: (textToCopy) => {
                            navigator.clipboard.writeText(textToCopy).catch(err => console.error('Copy failed:', err));
                        },
                        args: [request.data]
                    });
                }
                break;
            }
            case 'add': {
                const { wordlist, saveToWordList } = await getOptions();
                const currentList = wordlist || [];
                const saveFirstEntryOnly = saveToWordList === 'firstEntryOnly';

                for (const reqEntry of request.entries) {
                    currentList.push({
                        timestamp: Date.now(),
                        simplified: reqEntry.simplified,
                        traditional: reqEntry.traditional,
                        pinyin: reqEntry.pinyin,
                        definition: reqEntry.definition
                    });
                    if (saveFirstEntryOnly) break;
                }
                await chrome.storage.local.set({ wordlist: currentList });
                break;
            }
        }
    })();
    return true; // Indicates that the response is sent asynchronously
});
