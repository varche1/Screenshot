Ext.define('Screener.view.screen.List', {
    extend: 'Ext.tab.Panel',
    alias: 'widget.screenlist',
    
    //store: 'Sites',
    
    //title: 'Screens',
    defaults :{
        autoScroll: true,
        bodyPadding: 5
    },
    store: 'Pages',
    initComponent: function() {
        this.items = [{
            title: 'All',
            border: false,
            id: 'screen-all'
        },{
            title: 'Win7',
            border: false,
            id: 'screen-win7'
        },{
            title: 'WinXP',
            border: false,
            id: 'screen-winxp'
        },{
            title: 'Ubuntu',
            border: false,
            id: 'screen-ubuntu'
        }
            /*,
             url: '/screen?page=4f57ee94c6a8080824000001',
            {
            title: 'All',
            bodyPadding: 10,
            id: 'screen-all',
            items: dataview
        },{
            title: 'WinXP',
            bodyPadding: 10,
            id: 'screen-winxp',
            items: dataview
        },{
            title: 'Win7',
            bodyPadding: 10,
            id: 'screen-win7',
            items: dataview
        },{
            title: 'Ubuntu',
            bodyPadding: 10,
            id: 'screen-ubuntu',
            items: dataview
        }*/]
        
        this.callParent();
    }
});