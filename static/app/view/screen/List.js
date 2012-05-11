Ext.define('Screener.view.screen.List', {
    extend: 'Ext.Panel',
    alias: 'widget.screenlist',
    
    autoScroll: true,
    bodyPadding: 5,
    initComponent: function() {
        this.dockedItems = [{
            xtype: 'toolbar',
            items: [{
                xtype: 'button',
                text:'Win7',
                iconCls: 'os-win7',
                action: 'filter-os',
                value: 'win7',
                enableToggle: true
            },{
                xtype: 'button',
                text:'WinXP',
                iconCls: 'os-winxp',
                action: 'filter-os',
                value: 'winxp',
                enableToggle: true
            },'-',{
                xtype: 'button',
                text: 'Firefox',
                iconCls: 'browser-ff',
                action: 'filter-browser',
                value: 'ff',
                enableToggle: true
            },{
                xtype: 'button',
                text: 'IE',
                iconCls: 'browser-ie',
                action: 'filter-browser',
                value: 'ie',
                enableToggle: true
            },{
                xtype: 'button',
                text: 'Opera',
                iconCls: 'browser-op',
                action: 'filter-browser',
                value: 'op',
                enableToggle: true
            },{
                xtype: 'button',
                text: 'Chrome',
                iconCls: 'browser-ch',
                action: 'filter-browser',
                value: 'ch',
                enableToggle: true
            },{
                xtype: 'button',
                text: 'Safari',
                iconCls: 'browser-sf',
                action: 'filter-browser',
                value: 'sf',
                enableToggle: true
            }]
        }];
        
        this.callParent();
    }
});