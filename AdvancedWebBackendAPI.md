## Register [/register] [POST]

+ Request 

{
    id : (char max 100)
    password : (char max 100)
    name : (char max 100)
    role : ('STUDENT' or 'TEACHER')
}

+ Response 201
created
{}

+ Response 409
id confliction
{}

+ Response 400
other kind of error

## Login [/login] [POST]

+ Request

{
    id
    password
} 

+ Response 200

{
    id
    name
    role
}

+ Response 400

failure

{}

## Logout [/logout] [DELETE]

+ Request

{}

+ Response 200

{}

## Tree [/tree]

### Get Tree [GET]

+ Request

{}

+ Response 200

{ tree data }

+ Response 403

{
    detail:login first
}

+ Response 404
no tree

### Set Tree [POST]

+ Request

{ tree data }

+ Response 200

{}

+ Response 403

{
    detail:user not teacher
}

+ Response 403

{
    detail:login first
}

## Set Homework [/homework] [POST]

+ Request

{
    node_id : (id of the node of homework)
    published : (true or false)
    questions:[
        {
           type : ('CHOICE' or 'TEXT')
           question : (char max 100)
           A : (char max 100)
           B : (char max 100)
           C : (char max 100)
           D : (char max 100)
           correct_answer : (char max 100) 
        }
        ...
    ]
}

example

{
	"questions": [
		{
			"type": "TEXT",
			"question": "what the fuck",
			"A": null,
			"B": null,
			"C": null,
			"D": null,
			"correct_answer": null,
			"order": 0
		},
		{
			"type": "CHOICE",
			"question": "who the fuck",
			"A": "a",
			"B": "b",
			"C": "c",
			"D": "d",
			"correct_answer": "abc",
			"order": 0
		}
	],
	"published": false,
	"node_id": 10
}


+ Response 403

{
    detail:user not teacher
}

+ Response 403

{
    detail:login first
}

## Get Homework [/homework] [GET]

+ Request
{}

+ Response 200

{
	"questions": [
		{
			"id": 5,
			"type": "TEXT",
			"question": "what the fuck",
			"A": null,
			"B": null,
			"C": null,
			"D": null,
			"correct_answer": null,
			"order": 0
		},
		{
			"id": 6,
			"type": "CHOICE",
			"question": "who the fuck",
			"A": "a",
			"B": "b",
			"C": "c",
			"D": "d",
			"correct_answer": "abc",
			"order": 1
		}
	],
	"published": false,
	"node_id": 10
}

+ Response 403

{
    detail:login first
}

+ Response 404

{}

## Get Homework Answer of a student [/homework_answer/(node_id)] [GET]

+ Request

{}

+ Response 200

{
    "answers":[
        {
            "answer" : (answer text)
            "question" : (id of corresponding question)
        }
        ...
    ]
}

example

{
	"answers": [
		{
			"answer": "jalksdkjfioasdjhgpiowjrsopfgkj;pswjhb;p'ir5wnjmhp",
			"question": 5
		},
		{
			"answer": "l;sdkjfgkswjdiogw2pirjgkpowrkhgp-oeswrnjmhboieswjrghpijwrf",
			"question": 4
		}
	],
}

+ Response 403

{
    detail:user not student
}

+ Response 403

{
    detail:login first
}

+ Response 404

{}

## Set homework answer for a student [/homework_answer] [POST]

+ Request

{
	"node_id": 4,
	"answers": [
		{
			"answer": "aaaaaaaaaaaaa",
			"question": 5
		},
		{
			"answer": "ccccccccccccccc",
			"question": 4
		}
	]
}

+ Response 200

{}

+ Response 400

something wrong with the request data

{}

+ Response 404

no corresponding homework

{}

+ Response 403

{
    detail:user not student
}

+ Response 403

{
    detail:login first
}

## Get Material List of a Node [/materials/(node_id)] [GET]

+ Request

{}

+ Response 200

{
	"materials": [
		{
			"id": 1,
			"material_name": "pic1"
		},
		{
			"id": 2,
			"material_name": "233333333"
		},
		{
			"id": 3,
			"material_name": "6666666666"
		}
	],
	"id": 1
}

+ Response 403

{
    detail:login first
}

+ Response 404

{}

## Add a material [materials] [POST]

+ Request

{
	node_id (id of corresponding node)
	material_name (char max 100)
}

## Get a file [/downloadfile/(material_id)] [GET]

+ Request

{}

+ Response 

download file as an attachment

{}

+ Response 404

{}

+ Response 403

{
    detail:login first
}

