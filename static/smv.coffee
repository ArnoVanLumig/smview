CodeMirror.defineMode("smv", (config) ->
	reserved =
		keywords: ["MODULE", "main", "DEFINE", "MDEFINE", "CONSTANTS", "VAR", "IVAR", "FROZENVAR", "INIT", "TRANS", "INVAR", "SPEC", "CTLSPEC", "LTLSPEC", "PSLSPEC", "COMPUTE", "NAME", "INVARSPEC", "FAIRNESS", "JUSTICE", "COMPASSION", "ISA", "ASSIGN", "CONSTRAINT", "SIMPWFF", "CTLWFF", "LTLWFF", "PSLWFF", "COMPWFF", "IN", "MIN", "MAX", "MIRROR", "PRED", "PREDICATES"]
		types: ["process","array","of","boolean","integer","real","word","word1","bool","signed","unsigned","extend","resize","sizeof","uwconst","swconst"]
		predicates: ["EX","AX","EF","AF","EG","AG","E","F","O","G","H","X","Y","Z","A","U","S","V","T","BU","EBF","ABF","EBG","ABG"]
		operators: ["case","esac","mod","next","init","union","in","xor","xnor","self","count","running"]
		constants: ["TRUE", "FALSE"]

	token: (stream, state) ->
		if (stream.eatSpace())
			return null;

		if stream.match(/^\d+/)
			return "constants"

		if stream.match(/^\w*/)
			for r, v of reserved
				if stream.current() in v
					return r

		stream.next()
		return null
)