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
        '<tpl for=".">',
            '<div class="screenshot {id}">',
                '<span><b class="browser browser-{browser}">{version}</b></span>',
                '<span>{resolution}</span>',
                '<a href="{imageUrl}" target="_blank">',
                    '<img src="{thumbUrl}" />',
                '</a>',
            '</div>',
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
                //url: '/image?page=%p%&type=%t%'.replace('%p%', data._id).replace('%t%', 'thumb')
                (function(){
                    this.updateScreens(Ext.decode(response.responseText));
                }).call(self)
            }
        });
    },
    
    onScreensUpdate: function(data) {
        //this.updateScreens(data);
        log(data);
    },
    
    prepareData: function(data)
    {
        var result = {'all':[]};
        Ext.each(data.results, function(value, key) {
            var system = value.browser.split('_');
            if (!result[system[0]]) result[system[0]] = [];
            var data = {
                id          : value._id,
                os          : system[0],
                browser     : system[1],
                version     : system[2],
                resolution  : value.resolution.replace('_', '*'),
                imageUrl    : '/image?page=%p%&type=normal'.replace('%p%', value._id),
                thumbUrl    : '/image?page=%p%&type=thumb'.replace('%p%', value._id)
            };
            result[system[0]].push(data);
            result['all'].push(data);
        });
        return result;
    },
    
    updateScreens: function(data)
    {
        data = this.prepareData(data)
        var self = this;
        var view = this.getScreenList();
        Ext.Object.each(data, function(key, value) {
            var conteiner = view.down('#screen-'+key);
            if (conteiner && conteiner.body)
                self.tpl.overwrite(conteiner.body, value);
        });
    }
});
