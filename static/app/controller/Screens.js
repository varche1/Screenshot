Ext.define('Screener.controller.Screens', {
    extend: 'Ext.app.Controller',
    
    views: [
        'screen.List'
    ],
    
    refs: [{
        ref: 'screenList',
        selector: 'screenlist'
    }],
    
    tpl: Ext.create('Ext.XTemplate',
        '<tpl for="ready">',
            '<div class="screenshot" id="{id}">',
                '<span><b class="browser browser-{browser}">{version}</b></span>',
                '<span>{resolution}</span>',
                '<a href="{imageUrl}" target="_blank">',
                    '<img src="{thumbUrl}" />',
                '</a>',
            '</div>',
        '</tpl>',
        '<tpl for="wait">',
            '<div class="screenshot" id="{id}">',
                '<span><b class="browser browser-{browser}">{version}</b></span>',
                '<span>{resolution}</span>',
                '<img src="{thumbUrl}" />',
            '</div>',
        '</tpl>',
        '<tpl for="update">',
            '<span><b class="browser browser-{browser}">{version}</b></span>',
            '<span>{resolution}</span>',
            '<a href="{imageUrl}" target="_blank">',
                '<img src="{thumbUrl}" />',
            '</a>',
        '</tpl>'
    ),
    
    init: function() {
        this.control({});
        
        this.application.on({
            screenload: this.onScreensLoad,
            screenUpdate: this.onScreensUpdate,
            scope: this
        });
    },
    
    onScreensLoad: function(page) {
        if (!page || !page.get('_id'))
            return;
        
        var self = this;
        Ext.Ajax.request({
            method: 'GET',
            url: '/screen',
            params: { page: page.get('_id') },
            success: function(response){
                (function(){
                    this.updateScreens(Ext.decode(response.responseText));
                }).call(self)
            }
        });
    },
    
    onScreensUpdate: function(data) {
        data = this.prepareData({results: [data]})
        var self = this;
        var view = this.getScreenList();
        Ext.Object.each(data, function(key, value) {
            var screen = Ext.DomQuery.select('#'+value.id);
            if (screen.length)
                self.tpl.overwrite(screen[0], {'update':value});
        });
    },
    
    prepareData: function(data)
    {
        var result = {'wait': [], 'ready': []};
        Ext.each(data.results, function(value, key) {
            value.resolution = value.resolution.replace('_', '*');
            value.imageUrl   = '/image?screen=%p%&type=medium'.replace('%p%', value._id);
            value.thumbUrl   = '/image?screen=%p%&type=thumbnail'.replace('%p%', value._id);
            
            if (value.ready)
                result.ready.push(value);
            else
                result.wait.push(value);
        });
        return result;
    },
    
    updateScreens: function(data)
    {
        data = this.prepareData(data)
        var self = this;
        var view = this.getScreenList();
        self.tpl.overwrite(view.body, data);
    }
});
