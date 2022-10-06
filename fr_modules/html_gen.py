def gen_html(filelink,filename):
    link1="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Adobe Document Services PDF Embed API Sample</title>
        <meta charset="utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
        <meta id="viewport" name="viewport" content="width=device-width, initial-scale=1"/>
        <script type="text/javascript" src="index.js"></script>
    </head>
    <!-- Customize page layout style according to your need and PDF file for best viewing experience -->
    <body style="margin: 0px 0 0 0px;">
        <div id="adobe-dc-view" style="height: 850px; ;"></div>
    <script src="https://documentservices.adobe.com/view-sdk/viewer.js"></script>
    <script type="text/javascript">
        document.addEventListener("adobe_dc_view_sdk.ready", function(){ 
            var adobeDCView = new AdobeDC.View({clientId: "ec53503d261f40cbb2f99bfd276b21d2", divId: "adobe-dc-view"});
            adobeDCView.previewFile({
                content:{location: {url: '""" +str(filelink)+ """'}},
                metaData:{fileName: '"""+str(filename)+"""'}
            }, );
        });
    </script>


    </body>
    </html>

    """
    return link1