//AUTOGENERATED BY genForallN.py
  
#ifndef __DOMAIN_FORALL3_H__
#define __DOMAIN_FORALL3_H__

#include<RAJA/RAJA.hxx>



/******************************************************************
 *  Policy base class, forall3()
 ******************************************************************/

    template<typename LOOP_ORDER, typename POL_I, typename POL_J, typename POL_K>
    struct ForallPolicy3 {
      typedef LOOP_ORDER LoopOrder;
      typedef POL_I PolicyI;
      typedef POL_J PolicyJ;
      typedef POL_K PolicyK;
    };


/******************************************************************
 *  Default Executor for forall3()
 ******************************************************************/

    template<typename POLICY_I, typename POLICY_J, typename POLICY_K, typename TI, typename TJ, typename TK>
    class Forall3Executor {
      public:  
        template<typename BODY>
        inline void operator()(TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body) const {
          RAJA::forall<POLICY_I>(is_i, RAJA_LAMBDA(int i){
            exec(is_j, is_k, RAJA_LAMBDA(int j, int k){
              body(i, j, k);
            });
          });
        }

      private:
        Forall2Executor<POLICY_J, POLICY_K, TJ, TK> exec;
    };


/******************************************************************
 *  OpenMP Auto-Collapsing Executors for forall3()
 ******************************************************************/

#ifdef _OPENMP

    // OpenMP Executor with collapse(2)
    template<typename POLICY_K, typename TK>
    class Forall3Executor<RAJA::omp_parallel_for_exec, RAJA::omp_parallel_for_exec, POLICY_K, RAJA::RangeSegment, RAJA::RangeSegment, TK> {
      public:  
        template<typename BODY>
        inline void operator()(RAJA::RangeSegment const &is_i, RAJA::RangeSegment const &is_j, TK const &is_k, BODY const &body) const {
          int const i_start = is_i.getBegin();
          int const i_end   = is_i.getEnd();

          int const j_start = is_j.getBegin();
          int const j_end   = is_j.getEnd();

#pragma omp parallel for collapse(2)
          for(int i = i_start;i < i_end;++ i){
            for(int j = j_start;j < j_end;++ j){
              RAJA::forall<POLICY_K>(is_k, RAJA_LAMBDA(int k){
                body(i, j, k);
              });
          } } 
        }
    };

    // OpenMP Executor with collapse(3)
    template<>
    class Forall3Executor<RAJA::omp_parallel_for_exec, RAJA::omp_parallel_for_exec, RAJA::omp_parallel_for_exec, RAJA::RangeSegment, RAJA::RangeSegment, RAJA::RangeSegment> {
      public:  
        template<typename BODY>
        inline void operator()(RAJA::RangeSegment const &is_i, RAJA::RangeSegment const &is_j, RAJA::RangeSegment const &is_k, BODY const &body) const {
          int const i_start = is_i.getBegin();
          int const i_end   = is_i.getEnd();

          int const j_start = is_j.getBegin();
          int const j_end   = is_j.getEnd();

          int const k_start = is_k.getBegin();
          int const k_end   = is_k.getEnd();

#pragma omp parallel for collapse(3)
          for(int i = i_start;i < i_end;++ i){
            for(int j = j_start;j < j_end;++ j){
              for(int k = k_start;k < k_end;++ k){
                body(i, j, k);
          } } } 
        }
    };


#endif // _OPENMP


/******************************************************************
 *  Permutations layer for forall3()
 ******************************************************************/

      template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
      RAJA_INLINE void forall3_permute(PERM_IJK, TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
        Forall3Executor<typename POLICY::PolicyI, typename POLICY::PolicyJ, typename POLICY::PolicyK, TI, TJ, TK> exec;
        exec(is_i, is_j, is_k, RAJA_LAMBDA(int i, int j, int k){
          body(i, j, k);
        });
      }

      template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
      RAJA_INLINE void forall3_permute(PERM_IKJ, TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
        Forall3Executor<typename POLICY::PolicyI, typename POLICY::PolicyK, typename POLICY::PolicyJ, TI, TK, TJ> exec;
        exec(is_i, is_k, is_j, RAJA_LAMBDA(int i, int k, int j){
          body(i, j, k);
        });
      }

      template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
      RAJA_INLINE void forall3_permute(PERM_JIK, TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
        Forall3Executor<typename POLICY::PolicyJ, typename POLICY::PolicyI, typename POLICY::PolicyK, TJ, TI, TK> exec;
        exec(is_j, is_i, is_k, RAJA_LAMBDA(int j, int i, int k){
          body(i, j, k);
        });
      }

      template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
      RAJA_INLINE void forall3_permute(PERM_JKI, TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
        Forall3Executor<typename POLICY::PolicyJ, typename POLICY::PolicyK, typename POLICY::PolicyI, TJ, TK, TI> exec;
        exec(is_j, is_k, is_i, RAJA_LAMBDA(int j, int k, int i){
          body(i, j, k);
        });
      }

      template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
      RAJA_INLINE void forall3_permute(PERM_KIJ, TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
        Forall3Executor<typename POLICY::PolicyK, typename POLICY::PolicyI, typename POLICY::PolicyJ, TK, TI, TJ> exec;
        exec(is_k, is_i, is_j, RAJA_LAMBDA(int k, int i, int j){
          body(i, j, k);
        });
      }

      template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
      RAJA_INLINE void forall3_permute(PERM_KJI, TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
        Forall3Executor<typename POLICY::PolicyK, typename POLICY::PolicyJ, typename POLICY::PolicyI, TK, TJ, TI> exec;
        exec(is_k, is_j, is_i, RAJA_LAMBDA(int k, int j, int i){
          body(i, j, k);
        });
      }


/******************************************************************
 *  User interface, forall3()
 ******************************************************************/

    template<typename POLICY, typename TI, typename TJ, typename TK, typename BODY>
    RAJA_INLINE void forall3(TI const &is_i, TJ const &is_j, TK const &is_k, BODY const &body){
      typedef typename POLICY::LoopOrder L;
      forall3_permute<POLICY, TI, TJ, TK, BODY>(L(), is_i, is_j, is_k, body);
    }


  
#endif

