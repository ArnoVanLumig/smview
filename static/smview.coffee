knownMd5 = ""

markers = []

doRunTests = (code) ->
	$.ajax(
		type: "POST",
		url: "run",
		data:
			code: code
		success: (data) ->
			$("#right div.wrapper").html(data)
			knownMd5 = $("span.md5").text()
			$.bbq.pushState({ md5: knownMd5 });

			for marker in markers
				codeMirror.clearMarker(marker);
				codeMirror.setLineClass(marker, null, null);
			markers = []
			errors = $(".errorLine")
			if errors.length > 0
				for error in errors
					lineNo = +error.innerHTML.trim()
					console.log lineNo
					marker = codeMirror.setMarker(lineNo - 1, "●")
					codeMirror.setLineClass(marker, "", "errorline")
					markers.push(marker)
		error: () ->
			alert("nay")
	)

doRmUploader = () -> $("#uploader").remove()

runTests = _.debounce(doRunTests, 500)
rmUploader = _.once(doRmUploader)

codeMirrorChange = (editor, diff) ->
	code = editor.getValue()
	runTests(code)
	rmUploader()

codeArea = document.getElementById("codeArea")
codeMirror = CodeMirror.fromTextArea(codeArea,
			{
				lineNumbers: true
				autofocus: true
				gutter: true
				matchBrackets: true
				onChange: codeMirrorChange,
				mode: "smv"
			})

$(window).bind("hashchange", (e) ->
	md5 = $.bbq.getState("md5")
	if md5 != knownMd5 and md5?
		$.ajax(
			type: "GET",
			url: "getcode",
			data:
				md5: md5
			success: (data) ->
				codeMirror.setValue(data)
			error: () ->
				alert("nay")
		)
)

stopEvent = (evt) ->
	evt.stopPropagation();
	evt.preventDefault();

drop = (evt) ->
	evt.stopPropagation();
	evt.preventDefault();

	files = evt.dataTransfer.files;
	count = files.length;

	if count == 1
		file = files[0]
		reader = new FileReader()
		reader.onload = (evt2) ->
			code = evt2.target.result
			codeMirror.setValue(code)
		reader.readAsText(file)
	else
		alert("Please drag and drop a single file")

if typeof(String.prototype.trim) == "undefined"
	String.prototype.trim = () ->
		return String(this).replace(/^\s+|\s+$/g, '');

$(window).trigger( "hashchange" );

$(() ->
	dropbox = $("#uploader")[0]

	dropbox.addEventListener("dragenter", stopEvent)
	dropbox.addEventListener("dragexit", stopEvent)
	dropbox.addEventListener("dragover", stopEvent)
	dropbox.addEventListener("drop", drop)
)