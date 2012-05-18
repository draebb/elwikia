({
  appDir: 'site',
  baseUrl: 'assets/js',
  dir: 'site-built',
  //optimize: 'none',
  optimizeCss: 'none',
  wrap: true,
  modules: [
    {
      name: 'require',
      include: ['main', 'almond'],
    }
  ]
})
