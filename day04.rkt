#lang racket

(require qi)
(require rebellion/streaming/transducer)
(require rebellion/streaming/reducer)
(require syntax/parse/define)

; Similar to bundle, but it lets me make as many groups as I want
; Thanks to @countvajhula for the tip!
(define-qi-syntax-rule (bundle* [(index ...) f] ...)
  (-< (~> (select index ...) f) ...))

(define-flow parse (~> (string-split #rx"[-,]") △ (>< string->number)))

(define-flow overlap
             (~> (bundle* [(2 4) min]
                          [(1 3) max])
                 -
                 add1
                 (max 0)))

(define-flow size (~> X - add1))

(define-flow overlaps (~> parse overlap positive?))

(define-flow fully-overlaps
             (~> parse 
                 (-< overlap (group 2 size size))
                 (or (~> (select 1 2) =)
                     (~> (select 1 3) =))))

(define part-one (into-transduced (mapping fully-overlaps) (filtering identity) #:into into-count))

(define part-two (into-transduced (mapping overlaps) (filtering identity) #:into into-count))

; Take a file as a command line argument and set it as the default input port.
; Falls back to stdin if no file is provided.
;
; Inspired by python's fileinput module.
(define-syntax-parse-rule (with-fileinput rhs:expr)
  (command-line
    #:program "advent-of-code"
    #:args ([filename '()])
    (parameterize 
      ([current-input-port (if (null? filename) current-input-port (open-input-file filename))])
      rhs)))

(with-fileinput
  (transduce (in-lines) #:into (reducer-zip list part-one part-two)))
