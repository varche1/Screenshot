Ext.Loader.setConfig({enabled:true});
Ext.application({
    name: 'Screener',
    appFolder: '/static/app',
    
    controllers: ['Sites', 'Pages', 'Screens'],
    launch: function() {
        Ext.create('Ext.Viewport', {
            layout: 'border',
            title: 'Ext Layout Browser',
            items: [{
                xtype: 'box',
                id: 'header',
                region: 'north',
                html: '<h1> Ext.Layout.Browser</h1>',
                height: 30
            },{
                layout: 'fit',
                id: 'layout-browser',
                region:'west',
                border: false,
                split:true,
                margins: '0 0 5 5',
                width: 275,
                items: [{
                    xtype: 'sitelist',
                    flex: 1
                }]
            },{
                region: 'center',
                layout: 'border',
                margins: '0 5 5 0',
                border: false,
                items: [{
                    xtype: 'pagelist',
                    region: 'center',
                    collapsible: true,
                    flex: 1,
                    margins: '0 0 5 0'
                }, {
                    xtype: 'screenlist',
                    region: 'south',
                    flex: 1
                }]
            }]
        });
    }
});
var Tools = {
    getFieldFromModels: function(list, field) {
        var result = []
        for (i = 0, count = list.length; i < count; i++)
            result.push(list[0].get(field));
        return result;
    }
}

// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; args.callee = args.callee.caller; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};

// make it safe to use console.log always
(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());