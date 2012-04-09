Ext.define('Screener.view.screen.Edit', {
    extend: 'Ext.window.Window',
    alias: 'widget.shotsfilter',
    
    title       : 'Get ScreenShots',
    layout      : 'fit',
    autoShow    : true,
    modal       : true,
    
    initComponent: function() {
        
        var Win7 = getBrowserGroup('Windows 7', 'win7', false, [
            ['IE',       'ie', ['6', '7', '8', '9']],
            ['Firefox',  'ff', ['3.6', '4', '6', '9', '10']],
            ['Opera',    'op', ['10.5', '11']],
            ['Chrome',   'ch', ['16']],
            ['Safari',   'sf', ['5']]
        ]);
        
        var WinXP = getBrowserGroup('Windows XP', 'winXP', true, [
            ['IE',       'ie', ['6', '7', '8']],
            ['Firefox',  'ff', ['3.6', '4']],
            ['Opera',    'op', ['10.5', '11']],
            ['Chrome',   'ch', ['12']]
        ]);
        
        var Ubuntu = getBrowserGroup('Ubuntu 11.10', 'ub11.10', true, [
            ['Firefox',  'ff', ['3.6', '4']],
            ['Chrome',   'ch', ['16']]
        ]);
        
        var Res = {
            xtype: 'fieldset',
            title: 'Разрешение экрана',
            layout: 'anchor',
            padding: '10 5 5',
            defaults: {
                labelStyle: 'padding-left:4px;'
            },
            collapsible: false,
            items: [{
                xtype: 'checkboxgroup',
                fieldLabel: '',
                //cls: 'x-check-group-alt',
                padding: '0 10',
                columns: 4,
                items: [
                    {boxLabel: '1600x1200',  name: 'resolution', inputValue: '1600_900'},
                    {boxLabel: '1280x1024', name: 'resolution', inputValue: '1280_1024'},
                    {boxLabel: '1024x768',  name: 'resolution', inputValue: '1024_768'},
                    {boxLabel: '800x600',   name: 'resolution', inputValue: '800_600'},
                    {boxLabel: '1600x900', name: 'resolution', inputValue: '1600_1200'}
                ]
            }]
        };
        
        this.items = [{
            xtype: 'form',
            labelWidth: 120,
            border: false,
            bodyPadding: 10,
            width: 550,
            url: '/screen',
            fieldDefaults: {
                labelStyle: 'font-weight:bold'
            },
            defaults: {
                margins: '0 0 10 0'
            },
            items: [Res, Win7, WinXP, Ubuntu]
        }];

        this.buttons = [{
            text: 'Save',
            action: 'save',
            scope: this,
            handler: this.close
        },{
            text: 'Cancel',
            scope: this,
            handler: this.close
        }];
        
        this.callParent();
        
        function getBrowserGroup(title, osID, isHide, browsers) {
            var group = {
                xtype: 'fieldset',
                title: title,
                layout: 'anchor',
                padding: '10 5 5',
                defaults: {
                    labelStyle: 'padding-left:20px;'
                },
                collapsible: true,
                collapsed: isHide,
                items: []
            };
            
            for (b=0, cnt1 = browsers.length; b < cnt1; b++) {
                var versions = browsers[b][2];
                var brId = browsers[b][1];
                var tmp = {
                    xtype:      'checkboxgroup',
                    fieldLabel: browsers[b][0],
                    cls:        ((b % 2 ? 'x-check-group-alt ' : '') + 'browser browser-' + brId),
                    columns:    5,
                    items:      []
                };
                for (v=0, cnt2 = versions.length; v < cnt2; v++)
                    tmp.items.push({boxLabel: versions[v], name: 'browsers', inputValue: osID+'_'+brId+'_'+versions[v]})
                
                group.items.push(tmp);
            }
            
            return group;
        }
    }
});