/** @odoo-module */


import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";


publicWidget.registry.snippet_clicking_page = publicWidget.Widget.extend({
    selector: '.container',
    events: {
        'click .snippet': '_onClickSnippet',
    },

    _onClickSnippet: function(e){
        var clicked_event_id = $(e.currentTarget).children().children().html()
        window.location = `/event/${clicked_event_id}`;
    },

});



//export function chunk(array, size) {
//    const result = [];
//    for (let i = 0; i < array.length; i += size) {
//        result.push(array.slice(i, i + size));
//    }
//    return result;
//}

var RecentEvents = publicWidget.Widget.extend({
    selector: '.recent_event_snippet',

//    willStart: async function () {
//            console.log('hi')
//            const data = await jsonrpc('/recent-events', {})
//            const values = data
//            Object.assign(this, {
//                values
//            })
//        },

    start: function () {
        jsonrpc('/recent-events', {}).then((result) => {
        console.log('js')
        const refEl = this.$el.find("#recent_events")
        $(result['recent_events']).each(function(){
            var description = $(this.description).text()
            this.description = description
        })
        console.log(result)
        refEl.html(renderToElement('school_management.recent_event_wise', {
            result,
        }))
        })
    },
});
publicWidget.registry.recent_event_wise_snippet = RecentEvents;
return RecentEvents;