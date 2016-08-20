define([
  "dojo/_base/declare",
  "dojo/parser",
  "dojo/_base/lang",
  "dojo/dom-construct",
  "dijit/_WidgetBase",
  "dijit/_OnDijitClickMixin",
  "dijit/_TemplatedMixin",
  "dojo/text!./templates/HomepageBanner_template.html"
], function(
  declare,
  parser,
  lang,
  domConstruct,
  _WidgetBase,
  _OnDijitClickMixin,
  _TemplatedMixin,
  template
) {
  return declare([_WidgetBase, _OnDijitClickMixin, _TemplatedMixin], {
    templateString: template,
    options: {
      baseClass: null,
      title: null
    },

    constructor: function(options) {
      declare.safeMixin(this.options, options);
      this.set("baseClass", this.options.baseClass);
      this.set("title", this.options.title);
    },

    postCreate: function() {
    }


  });
});
