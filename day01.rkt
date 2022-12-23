#lang racket

(require rebellion/streaming/transducer)
(require rebellion/streaming/reducer)
(require syntax/parse/define)

(define batch-elves (batching (into-transduced (taking-while non-empty-string?)
                                               (mapping string->number)
                                               #:into into-sum)))

(define part-one
  (into-transduced batch-elves
                   #:into (into-max)))

(define part-two
  (into-transduced batch-elves
                   (sorting #:descending? #t)
                   (taking 3)
                   #:into into-sum))

; Take a file as a command line argument and set it as the default input port.
; Falls back to stdin if no file is provided.
;
; Inspired by python's fileinput module.
(define-syntax-parse-rule (with-fileinput rhs:expr)
  (command-line
    #:program "advent-of-code"
    #:args ([filename '()])
    (parameterize 
      ([current-input-port (if (null? filename)
                               current-input-port
                               (open-input-file filename))])
      rhs)))

(with-fileinput
  (transduce (in-lines) #:into (reducer-zip list part-one part-two)))
