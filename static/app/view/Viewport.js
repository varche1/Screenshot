Ext.define('Screener.view.Viewport', {
    extend: 'Ext.container.Viewport',
    layout: 'fit',
    
    requires: [
        //'Screener.view.NewStation',
        //'Screener.view.SongControls',
        'Screener.view.site.List',
        //'Screener.view.RecentlyPlayedScroller',
        //'Screener.view.SongInfo'
    ],
    
    initComponent: function() {
        this.items = {
            xtype: 'siteslist'
            /*
            layout: {
                type: 'hbox',
                align: 'stretch'
            },
            items: [{
                width: 250,
                xtype: 'panel',
                id: 'west-region',
                layout: {
                    type: 'vbox',
                    align: 'stretch'
                },
                items: [{
                    xtype: 'siteslist',
                    flex: 1
                }]
            }]
            */
        };
        
        this.callParent();
    }
});