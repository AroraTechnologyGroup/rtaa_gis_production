define([
  "widgets/App"
], function(App) {

  const { assert } = intern.getPlugin('chai');
  const { describe, it } = intern.getInterface('bdd');

  describe('App', () => {
    it('should not throw when created', () => {
      assert.doesNotThrow(() => new App());
    });
  });
});