define([
  "dojo/_base/declare",
  "dojo/dom-construct",
  "dojo/parser",
  "dojo/ready",
  "dijit/_WidgetBase",
  "dijit/_OnDijitClickMixin",
  "dijit/_TemplatedMixin",
  "dojo/text!./templates/Card_template.html"
], function(
  declare,
  domConstruct,
  parser,
  ready,
  _WidgetBase,
  _OnDijitClickMixin,
  _TemplatedMixin,
  template
) {

  return declare([_WidgetBase, _TemplatedMixin], {
    templateString: template,
    options: {
      baseClass: null,
      imgSrc: null,
      header: null,
      contents: null
    },
    constructor: function(options, srcNodeRef) {
      this.inherited(arguments);
      declare.safeMixin(this.options, options);
      this.set("baseClass", this.options.baseClass);
      this.set("imgSrc", this.options.imgSrc);
      this.set("header", this.options.header);
      this.set("contents", this.options.contents);
      this.set("srcNodeRef", this.srcNodeRef);
    }
  });
});
